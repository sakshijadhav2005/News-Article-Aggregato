"""Real article storage service using MongoDB with async Motor"""
import logging
import json
from typing import List, Optional, Tuple
from datetime import datetime, timedelta
import uuid
import re

from ..models.article import Article, QueryFilters
from ..core.exceptions import ArticleNotFoundError, DatabaseError
from ..core.error_handler import handle_errors

logger = logging.getLogger(__name__)

# Try to import DB module; fall back to in-memory if not available
_db_available = False

try:
    from ..db import get_db
    _db_available = True
except ImportError:
    logger.warning("Database module not available, using in-memory storage")


class ArticleStore:
    """
    Production article storage service.
    Uses MongoDB when available, falls back to in-memory storage.
    """

    def __init__(self):
        """Initialize storage"""
        self._memory_articles: dict[str, Article] = {}
        self._use_db = _db_available
        logger.info(f"ArticleStore initialized ({'MongoDB' if self._use_db else 'in-memory'} mode)")

    @handle_errors
    async def save_article(self, article: Article) -> str:
        """
        Save article to storage.

        Args:
            article: Article to save

        Returns:
            Article ID
        """
        if not article.id:
            article.id = str(uuid.uuid4())

        if self._use_db:
            try:
                db = await get_db()
                collection = db["articles"]

                # Check if article already exists (by URL or content hash)
                existing = await collection.find_one({
                    "$or": [
                        {"url": article.url},
                        {"content_hash": article.content_hash or ""}
                    ]
                })

                if existing:
                    # Update existing article
                    update_doc = self._to_document(article)
                    update_doc.pop("_id", None)
                    await collection.update_one(
                        {"_id": existing["_id"]},
                        {"$set": update_doc}
                    )
                    logger.debug(f"Updated existing article: {article.title}")
                    return article.id

                # Insert new article
                doc = self._to_document(article)
                await collection.insert_one(doc)
                logger.info(f"Saved article to MongoDB: {article.id}")
                return article.id

            except Exception as e:
                logger.error(f"MongoDB save failed, falling back to memory: {e}")

        # In-memory fallback
        self._memory_articles[article.id] = article
        logger.info(f"Saved article to memory: {article.id}: {article.title}")
        return article.id

    @handle_errors
    async def get_article(self, article_id: str) -> Article:
        """
        Get article by ID.

        Args:
            article_id: Article ID

        Returns:
            Article object

        Raises:
            ArticleNotFoundError: If article not found
        """
        if self._use_db:
            try:
                db = await get_db()
                collection = db["articles"]

                doc = await collection.find_one({"id": article_id})
                if doc:
                    return self._to_article(doc)
            except Exception as e:
                logger.error(f"MongoDB get failed: {e}")

        # In-memory fallback
        article = self._memory_articles.get(article_id)
        if not article:
            raise ArticleNotFoundError(f"Article {article_id} not found")
        return article

    @handle_errors
    async def query_articles(
        self,
        filters: QueryFilters,
        page: int = 1,
        page_size: int = 20
    ) -> Tuple[List[Article], int]:
        """
        Query articles with filters and pagination.

        Args:
            filters: Query filters
            page: Page number (1-indexed)
            page_size: Items per page

        Returns:
            Tuple of (articles list, total count)
        """
        if self._use_db:
            try:
                db = await get_db()
                collection = db["articles"]

                # Build MongoDB filter
                query = {}
                conditions = []

                if filters.source:
                    conditions.append({"source": filters.source})
                if filters.date_from:
                    conditions.append({"published_date": {"$gte": filters.date_from}})
                if filters.date_to:
                    conditions.append({"published_date": {"$lte": filters.date_to}})
                if filters.cluster_id is not None:
                    conditions.append({"cluster_id": filters.cluster_id})
                if filters.search_text:
                    conditions.append({"title": {"$regex": re.escape(filters.search_text), "$options": "i"}})

                if conditions:
                    query = {"$and": conditions}

                # Get total count
                total = await collection.count_documents(query)

                # Apply ordering and pagination
                offset = (page - 1) * page_size
                cursor = collection.find(query).sort("published_date", -1).skip(offset).limit(page_size)
                docs = await cursor.to_list(length=page_size)

                articles = [self._to_article(doc) for doc in docs]

                logger.info(f"MongoDB query returned {len(articles)} articles (total: {total})")
                return articles, total

            except Exception as e:
                logger.error(f"MongoDB query failed: {e}")

        # In-memory fallback
        filtered = list(self._memory_articles.values())

        if filters.source:
            filtered = [a for a in filtered if a.source == filters.source]
        if filters.date_from:
            filtered = [a for a in filtered if a.published_date >= filters.date_from]
        if filters.date_to:
            filtered = [a for a in filtered if a.published_date <= filters.date_to]
        if filters.cluster_id is not None:
            filtered = [a for a in filtered if a.cluster_id == filters.cluster_id]
        if filters.search_text:
            search_lower = filters.search_text.lower()
            filtered = [a for a in filtered if search_lower in a.title.lower()]

        filtered.sort(key=lambda a: a.published_date, reverse=True)

        total = len(filtered)
        start = (page - 1) * page_size
        end = start + page_size
        paginated = filtered[start:end]

        logger.info(f"Memory query returned {len(paginated)} articles (total: {total})")
        return paginated, total

    @handle_errors
    async def get_articles_by_cluster(self, cluster_id: int) -> List[Article]:
        """Get all articles in a cluster"""
        if self._use_db:
            try:
                db = await get_db()
                collection = db["articles"]

                cursor = collection.find({"cluster_id": cluster_id}).sort("published_date", -1)
                docs = await cursor.to_list(length=1000)
                return [self._to_article(doc) for doc in docs]
            except Exception as e:
                logger.error(f"MongoDB cluster query failed: {e}")

        return [a for a in self._memory_articles.values() if a.cluster_id == cluster_id]

    async def get_all_articles(self) -> List[Article]:
        """Get all articles"""
        if self._use_db:
            try:
                db = await get_db()
                collection = db["articles"]

                cursor = collection.find().sort("published_date", -1)
                docs = await cursor.to_list(length=10000)
                return [self._to_article(doc) for doc in docs]
            except Exception as e:
                logger.error(f"MongoDB get all failed: {e}")

        return list(self._memory_articles.values())

    async def count_articles(self) -> int:
        """Get total article count"""
        if self._use_db:
            try:
                db = await get_db()
                collection = db["articles"]
                return await collection.count_documents({})
            except Exception as e:
                logger.error(f"MongoDB count failed: {e}")

        return len(self._memory_articles)

    async def archive_old_articles(self, days: int = 30) -> int:
        """Archive articles older than specified days"""
        cutoff = datetime.now() - timedelta(days=days)
        archived = 0

        if self._use_db:
            try:
                db = await get_db()
                collection = db["articles"]

                result = await collection.delete_many({"published_date": {"$lt": cutoff}})
                archived = result.deleted_count
                logger.info(f"Archived {archived} articles older than {days} days")
            except Exception as e:
                logger.error(f"Archive failed: {e}")
        else:
            old_ids = [
                aid for aid, a in self._memory_articles.items()
                if a.published_date < cutoff
            ]
            for aid in old_ids:
                del self._memory_articles[aid]
            archived = len(old_ids)

        return archived

    def _to_document(self, article: Article) -> dict:
        """Convert Article dataclass to MongoDB document"""
        embedding_json = None
        if article.embedding is not None:
            try:
                embedding_json = json.dumps(article.embedding.tolist())
            except Exception:
                pass

        return {
            "id": article.id,
            "url": article.url,
            "content_hash": article.content_hash or "",
            "title": article.title,
            "compressed_content": article.compressed_content,
            "summary": article.summary,
            "source": article.source,
            "author": article.author,
            "published_date": article.published_date,
            "fetched_date": article.fetched_date,
            "cluster_id": article.cluster_id,
            "embedding": embedding_json,
        }

    def _to_article(self, doc: dict) -> Article:
        """Convert MongoDB document to Article dataclass"""
        import numpy as np

        embedding = None
        if doc.get("embedding"):
            try:
                embedding = np.array(json.loads(doc["embedding"]))
            except Exception:
                pass

        return Article(
            id=doc.get("id", str(doc.get("_id", ""))),
            url=doc["url"],
            title=doc["title"],
            compressed_content=doc["compressed_content"],
            summary=doc.get("summary"),
            source=doc["source"],
            author=doc.get("author"),
            published_date=doc["published_date"],
            fetched_date=doc.get("fetched_date", datetime.now()),
            cluster_id=doc.get("cluster_id"),
            embedding=embedding,
            content_hash=doc.get("content_hash"),
        )
