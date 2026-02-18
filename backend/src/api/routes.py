"""API routes with async handlers and caching"""
from fastapi import APIRouter, HTTPException, Query, Path
from typing import Optional
from datetime import datetime
import logging

from .responses import APIResponse, PaginatedResponse, ErrorResponse
from ..models.article import QueryFilters
from ..core.exceptions import ArticleNotFoundError

logger = logging.getLogger(__name__)

router = APIRouter()


def _get_pipeline():
    """Get the global pipeline instance"""
    from ..main import get_pipeline
    return get_pipeline()


# Health check endpoint
@router.get("/health")
async def health_check():
    """Health check endpoint"""
    pipeline = _get_pipeline()
    stats = await pipeline.get_stats()

    return APIResponse(
        data={
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "stats": stats,
        },
        message="News Article Aggregator API is running"
    ).dict()


# Get articles with filtering and pagination
@router.get("/articles")
async def get_articles(
    source: Optional[str] = Query(None, description="Filter by source"),
    date_from: Optional[str] = Query(None, description="Filter from date (ISO format)"),
    date_to: Optional[str] = Query(None, description="Filter to date (ISO format)"),
    search: Optional[str] = Query(None, description="Search text in titles"),
    cluster_id: Optional[int] = Query(None, description="Filter by cluster"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page")
):
    """
    Get articles with filtering and pagination.
    Async handler with caching and proper error handling.
    """
    pipeline = _get_pipeline()

    try:
        # Build cache key
        cache_key = f"query:{source}:{date_from}:{date_to}:{search}:{cluster_id}:{page}:{page_size}"

        # Try cache first
        cached = await pipeline.cache.get(cache_key)
        if cached:
            return cached

        # Parse dates
        parsed_date_from = None
        parsed_date_to = None

        if date_from:
            try:
                parsed_date_from = datetime.fromisoformat(date_from)
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid date_from format: {date_from}. Use ISO 8601 format."
                )

        if date_to:
            try:
                parsed_date_to = datetime.fromisoformat(date_to)
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid date_to format: {date_to}. Use ISO 8601 format."
                )

        # Build filters
        filters = QueryFilters(
            source=source,
            date_from=parsed_date_from,
            date_to=parsed_date_to,
            cluster_id=cluster_id,
            search_text=search,
        )

        # Query articles
        articles, total = await pipeline.store.query_articles(filters, page, page_size)

        # Format response
        articles_data = [
            {
                "id": a.id,
                "title": a.title,
                "summary": a.summary or "",
                "source": a.source,
                "author": a.author,
                "published_date": a.published_date.isoformat() if a.published_date else None,
                "url": a.url,
                "cluster_id": a.cluster_id,
            }
            for a in articles
        ]

        response = PaginatedResponse(
            data=articles_data,
            total=total,
            page=page,
            page_size=page_size,
            message=f"Found {total} articles"
        ).dict()

        # Cache response for 15 minutes
        await pipeline.cache.set(cache_key, response, ttl=900)

        return response

    except HTTPException:
        raise
    except ArticleNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error fetching articles: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# Get a specific article by ID
@router.get("/articles/{article_id}")
async def get_article(
    article_id: str = Path(..., description="Article ID")
):
    """Get a specific article by ID"""
    pipeline = _get_pipeline()

    try:
        # Try cache
        cache_key = f"article:{article_id}"
        cached = await pipeline.cache.get(cache_key)
        if cached:
            return cached

        article = await pipeline.store.get_article(article_id)

        # Decompress content
        content = ""
        try:
            content = pipeline.compressor.decompress(article.compressed_content)
        except Exception:
            content = "(Content unavailable)"

        article_data = {
            "id": article.id,
            "title": article.title,
            "content": content,
            "summary": article.summary or "",
            "source": article.source,
            "author": article.author,
            "published_date": article.published_date.isoformat() if article.published_date else None,
            "fetched_date": article.fetched_date.isoformat() if article.fetched_date else None,
            "url": article.url,
            "cluster_id": article.cluster_id,
        }

        response = APIResponse(
            data=article_data,
            message="Article retrieved successfully"
        ).dict()

        # Cache for 1 hour
        await pipeline.cache.set(cache_key, response, ttl=3600)
        return response

    except ArticleNotFoundError:
        raise HTTPException(status_code=404, detail=f"Article {article_id} not found")
    except Exception as e:
        logger.error(f"Error getting article {article_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# Get article summary
@router.get("/articles/{article_id}/summary")
async def get_article_summary(
    article_id: str = Path(..., description="Article ID")
):
    """Get article summary - generates on-demand if not cached"""
    pipeline = _get_pipeline()

    try:
        # Try cache
        cache_key = f"summary:{article_id}"
        cached = await pipeline.cache.get(cache_key)
        if cached:
            return cached

        article = await pipeline.store.get_article(article_id)

        # If no summary, generate one on the fly
        summary = article.summary
        if not summary:
            try:
                content = pipeline.compressor.decompress(article.compressed_content)
                summary = pipeline.summarizer.summarize(content)
                article.summary = summary
                await pipeline.store.save_article(article)
            except Exception as e:
                logger.warning(f"On-demand summarization failed: {e}")
                summary = "(Summary unavailable)"

        response = APIResponse(
            data={
                "article_id": article.id,
                "title": article.title,
                "summary": summary,
            },
            message="Summary retrieved successfully"
        ).dict()

        # Cache for 1 hour
        await pipeline.cache.set(cache_key, response, ttl=3600)
        return response

    except ArticleNotFoundError:
        raise HTTPException(status_code=404, detail=f"Article {article_id} not found")
    except Exception as e:
        logger.error(f"Error getting summary for {article_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# Get all topic clusters
@router.get("/clusters")
async def get_clusters():
    """Get all topic clusters"""
    pipeline = _get_pipeline()

    try:
        # Try cache
        cache_key = "clusters:all"
        cached = await pipeline.cache.get(cache_key)
        if cached:
            return cached

        clusters = pipeline.clusterer.get_all_clusters()

        clusters_data = [
            {
                "id": c.id,
                "label": c.label,
                "article_count": c.article_count,
                "created_at": c.created_at.isoformat() if c.created_at else None,
                "updated_at": c.updated_at.isoformat() if c.updated_at else None,
            }
            for c in clusters
        ]

        response = APIResponse(
            data=clusters_data,
            message=f"Found {len(clusters_data)} clusters"
        ).dict()

        # Cache for 30 minutes
        await pipeline.cache.set(cache_key, response, ttl=1800)
        return response

    except Exception as e:
        logger.error(f"Error fetching clusters: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# Get articles in a specific cluster
@router.get("/clusters/{cluster_id}/articles")
async def get_cluster_articles(
    cluster_id: int = Path(..., description="Cluster ID"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100)
):
    """Get articles in a specific cluster"""
    pipeline = _get_pipeline()

    try:
        # Try cache
        cache_key = f"cluster:{cluster_id}:articles:{page}:{page_size}"
        cached = await pipeline.cache.get(cache_key)
        if cached:
            return cached

        # Check cluster exists
        cluster = pipeline.clusterer.get_cluster(cluster_id)
        if not cluster:
            raise HTTPException(status_code=404, detail=f"Cluster {cluster_id} not found")

        # Get articles using filters
        filters = QueryFilters(cluster_id=cluster_id)
        articles, total = await pipeline.store.query_articles(filters, page, page_size)

        articles_data = [
            {
                "id": a.id,
                "title": a.title,
                "summary": a.summary or "",
                "source": a.source,
                "author": a.author,
                "published_date": a.published_date.isoformat() if a.published_date else None,
                "url": a.url,
                "cluster_id": a.cluster_id,
            }
            for a in articles
        ]

        response = PaginatedResponse(
            data=articles_data,
            total=total,
            page=page,
            page_size=page_size,
            message=f"Found {total} articles in cluster '{cluster.label}'"
        ).dict()

        # Cache for 30 minutes
        await pipeline.cache.set(cache_key, response, ttl=1800)
        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting cluster {cluster_id} articles: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# Trigger manual article fetch (admin endpoint)
@router.post("/articles/fetch")
async def trigger_fetch(
    count: int = Query(20, ge=1, le=100, description="Number of articles to fetch")
):
    """
    Trigger manual article fetch (admin endpoint).
    Runs the full processing pipeline.
    """
    pipeline = _get_pipeline()

    try:
        logger.info(f"Manual fetch triggered for {count} articles")
        results = await pipeline.process_articles(count=count)

        return APIResponse(
            data=results,
            message=f"Fetch complete: {results['stored']} articles processed"
        ).dict()

    except Exception as e:
        logger.error(f"Manual fetch failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Fetch failed: {str(e)}"
        )


# Get system stats
@router.get("/stats")
async def get_stats():
    """Get system statistics"""
    pipeline = _get_pipeline()

    try:
        stats = await pipeline.get_stats()
        return APIResponse(
            data=stats,
            message="System statistics"
        ).dict()
    except Exception as e:
        logger.error(f"Error getting stats: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
