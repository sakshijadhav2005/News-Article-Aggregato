"""Tests for Article Store (in-memory mode)"""
import pytest
import asyncio
from datetime import datetime, timedelta
import uuid
from src.services.store import ArticleStore
from src.models.article import Article, QueryFilters
from src.core.exceptions import ArticleNotFoundError


def _make_article(title="Test Article", source="Test Source", days_ago=0, cluster_id=None):
    """Helper to create test articles"""
    return Article(
        id=str(uuid.uuid4()),
        url=f"https://example.com/{uuid.uuid4()}",
        title=title,
        compressed_content=b"compressed_content_bytes",
        summary=f"Summary of {title}",
        source=source,
        author="Test Author",
        published_date=datetime.now() - timedelta(days=days_ago),
        fetched_date=datetime.now(),
        cluster_id=cluster_id,
        content_hash=str(uuid.uuid4()),
    )


@pytest.fixture
def store():
    s = ArticleStore()
    s._use_db = False  # Force in-memory mode for testing
    return s


class TestArticleStore:
    """Unit tests for ArticleStore"""

    @pytest.mark.asyncio
    async def test_save_and_retrieve(self, store):
        article = _make_article("Test Article 1")
        article_id = await store.save_article(article)
        assert article_id == article.id

        retrieved = await store.get_article(article_id)
        assert retrieved.title == "Test Article 1"

    @pytest.mark.asyncio
    async def test_get_nonexistent_article(self, store):
        with pytest.raises(ArticleNotFoundError):
            await store.get_article("nonexistent-id")

    @pytest.mark.asyncio
    async def test_query_no_filters(self, store):
        for i in range(5):
            await store.save_article(_make_article(f"Article {i}"))

        articles, total = await store.query_articles(QueryFilters())
        assert total == 5
        assert len(articles) == 5

    @pytest.mark.asyncio
    async def test_query_by_source(self, store):
        await store.save_article(_make_article("A1", source="BBC"))
        await store.save_article(_make_article("A2", source="CNN"))
        await store.save_article(_make_article("A3", source="BBC"))

        articles, total = await store.query_articles(QueryFilters(source="BBC"))
        assert total == 2

    @pytest.mark.asyncio
    async def test_query_by_search_text(self, store):
        await store.save_article(_make_article("AI Technology Breakthrough"))
        await store.save_article(_make_article("Climate Change Report"))
        await store.save_article(_make_article("New AI Model Released"))

        articles, total = await store.query_articles(
            QueryFilters(search_text="AI")
        )
        assert total == 2

    @pytest.mark.asyncio
    async def test_query_by_cluster(self, store):
        await store.save_article(_make_article("A1", cluster_id=1))
        await store.save_article(_make_article("A2", cluster_id=2))
        await store.save_article(_make_article("A3", cluster_id=1))

        articles, total = await store.query_articles(
            QueryFilters(cluster_id=1)
        )
        assert total == 2

    @pytest.mark.asyncio
    async def test_pagination(self, store):
        for i in range(25):
            await store.save_article(_make_article(f"Article {i}"))

        page1, total = await store.query_articles(QueryFilters(), page=1, page_size=10)
        assert len(page1) == 10
        assert total == 25

        page3, _ = await store.query_articles(QueryFilters(), page=3, page_size=10)
        assert len(page3) == 5

    @pytest.mark.asyncio
    async def test_archive_old_articles(self, store):
        await store.save_article(_make_article("Recent", days_ago=5))
        await store.save_article(_make_article("Old", days_ago=45))
        await store.save_article(_make_article("Very Old", days_ago=60))

        archived = await store.archive_old_articles(days=30)
        assert archived == 2

        count = await store.count_articles()
        assert count == 1

    @pytest.mark.asyncio
    async def test_count_articles(self, store):
        assert await store.count_articles() == 0
        await store.save_article(_make_article("A1"))
        assert await store.count_articles() == 1

    @pytest.mark.asyncio
    async def test_get_articles_by_cluster(self, store):
        await store.save_article(_make_article("A1", cluster_id=5))
        await store.save_article(_make_article("A2", cluster_id=5))
        await store.save_article(_make_article("A3", cluster_id=3))

        articles = await store.get_articles_by_cluster(5)
        assert len(articles) == 2
