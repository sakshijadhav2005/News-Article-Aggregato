"""Main processing pipeline - wires all services together"""
import logging
import uuid
from typing import List, Optional
from datetime import datetime

from ..models.article import Article, RawArticle
from ..services.compressor import ContentCompressor
from ..services.fetcher import ArticleFetcher
from ..services.summarizer import Summarizer
from ..services.clusterer import TopicClusterer
from ..services.store import ArticleStore
from ..services.cache import CacheManager

logger = logging.getLogger(__name__)


class Pipeline:
    """
    Main processing pipeline.
    Orchestrates: Fetch → Compress → Store → Summarize → Cluster
    """

    def __init__(self):
        from config.settings import settings

        self.compressor = ContentCompressor()
        self.fetcher = ArticleFetcher(
            newsapi_key=settings.fetcher.newsapi_key,
            rss_feeds=settings.fetcher.rss_feeds,
            timeout=settings.fetcher.timeout,
            max_retries=settings.fetcher.max_retries,
            min_content_words=settings.fetcher.min_content_words,
        )
        self.summarizer = Summarizer(
            model_name=settings.summarizer.model_name,
            max_length=settings.summarizer.max_summary_words,
            use_gpu=settings.summarizer.use_gpu,
            num_beams=settings.summarizer.num_beams,
        )
        self.clusterer = TopicClusterer(
            embedding_model_name=settings.clusterer.embedding_model,
            min_cluster_size=settings.clusterer.min_cluster_size,
            min_samples=settings.clusterer.min_samples,
            max_cluster_articles=settings.clusterer.max_cluster_articles,
            similarity_threshold=settings.clusterer.similarity_threshold,
        )
        self.store = ArticleStore()
        self.cache = CacheManager()

        logger.info("Processing pipeline initialized")

    async def process_articles(self, count: int = 50) -> dict:
        """
        Run the full processing pipeline.

        Args:
            count: Number of articles to fetch

        Returns:
            Processing results summary
        """
        results = {
            "fetched": 0,
            "stored": 0,
            "summarized": 0,
            "clustered": 0,
            "errors": [],
        }

        try:
            # Step 1: Fetch articles
            logger.info(f"Pipeline: Fetching up to {count} articles...")
            raw_articles = self.fetcher.fetch_articles(count=count)
            results["fetched"] = len(raw_articles)
            logger.info(f"Pipeline: Fetched {len(raw_articles)} articles")

            if not raw_articles:
                logger.warning("No articles fetched")
                return results

            # Step 2: Compress and store articles
            stored_articles = []
            for raw in raw_articles:
                try:
                    article = self._process_raw_article(raw)
                    article_id = await self.store.save_article(article)
                    article.id = article_id
                    stored_articles.append(article)
                    results["stored"] += 1
                except Exception as e:
                    logger.error(f"Failed to process article '{raw.title}': {e}")
                    results["errors"].append(f"Store: {raw.title} - {str(e)}")

            logger.info(f"Pipeline: Stored {len(stored_articles)} articles")

            # Step 3: Generate summaries
            for article in stored_articles:
                try:
                    content = self.compressor.decompress(article.compressed_content)
                    summary = self.summarizer.summarize(content)
                    article.summary = summary
                    await self.store.save_article(article)
                    results["summarized"] += 1
                except Exception as e:
                    logger.error(f"Summarization failed for '{article.title}': {e}")
                    results["errors"].append(f"Summary: {article.title} - {str(e)}")

            logger.info(f"Pipeline: Summarized {results['summarized']} articles")

            # Step 4: Cluster articles
            try:
                all_articles = await self.store.get_all_articles()
                if all_articles:
                    cluster_map = self.clusterer.cluster_articles(all_articles)
                    results["clustered"] = len(cluster_map)

                    # Update articles with cluster assignments
                    for article in all_articles:
                        if article.cluster_id is not None:
                            await self.store.save_article(article)

                    logger.info(f"Pipeline: Created {len(cluster_map)} clusters")
            except Exception as e:
                logger.error(f"Clustering failed: {e}")
                results["errors"].append(f"Clustering: {str(e)}")

            # Step 5: Invalidate cache
            await self.cache.clear()
            logger.info("Pipeline: Cache cleared after processing")

        except Exception as e:
            logger.error(f"Pipeline error: {e}")
            results["errors"].append(f"Pipeline: {str(e)}")

        return results

    def _process_raw_article(self, raw: RawArticle) -> Article:
        """Convert raw article to stored article with compression"""
        compressed = self.compressor.compress(raw.content)

        return Article(
            id=str(uuid.uuid4()),
            url=raw.url,
            title=raw.title,
            compressed_content=compressed,
            summary=None,
            source=raw.source,
            author=raw.author,
            published_date=raw.published_date,
            fetched_date=datetime.now(),
            cluster_id=None,
            embedding=None,
            content_hash=raw.content_hash,
        )

    async def get_stats(self) -> dict:
        """Get system statistics"""
        article_count = await self.store.count_articles()
        cluster_count = len(self.clusterer.clusters)
        cache_size = await self.cache.size()

        return {
            "total_articles": article_count,
            "total_clusters": cluster_count,
            "cache_size": cache_size,
            "sources": list(set(
                a.source for a in (await self.store.get_all_articles())
            )) if article_count > 0 else [],
        }
