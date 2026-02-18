"""Tests for Article Fetcher"""
import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from src.services.fetcher import ArticleFetcher
from src.models.article import RawArticle


class TestArticleFetcher:
    """Unit tests for ArticleFetcher"""

    def setup_method(self):
        self.fetcher = ArticleFetcher(
            rss_feeds=["https://feeds.bbci.co.uk/news/rss.xml"],
            timeout=5,
            max_retries=1,
            min_content_words=10,
        )

    def test_initialization(self):
        assert len(self.fetcher.rss_feeds) == 1
        assert self.fetcher.timeout == 5

    def test_deduplicate_by_url(self):
        articles = [
            RawArticle(
                url="https://example.com/article1",
                title="Article 1",
                content="Content for article one is here and it has enough words.",
                source="Test",
                published_date=datetime.now(),
            ),
            RawArticle(
                url="https://example.com/article1",  # Same URL
                title="Article 1 Duplicate",
                content="Different content for the same URL article duplicate.",
                source="Test",
                published_date=datetime.now(),
            ),
        ]
        unique = self.fetcher.deduplicate(articles)
        assert len(unique) == 1

    def test_deduplicate_by_content_hash(self):
        same_content = "Identical content for testing deduplication by hash."
        articles = [
            RawArticle(
                url="https://example.com/article1",
                title="Article 1",
                content=same_content,
                source="Source A",
                published_date=datetime.now(),
            ),
            RawArticle(
                url="https://example.com/article2",
                title="Article 2",
                content=same_content,
                source="Source B",
                published_date=datetime.now(),
            ),
        ]
        unique = self.fetcher.deduplicate(articles)
        assert len(unique) == 1

    def test_deduplicate_unique_articles(self):
        articles = [
            RawArticle(
                url=f"https://example.com/article{i}",
                title=f"Article {i}",
                content=f"Unique content for article number {i} with enough words here.",
                source="Test",
                published_date=datetime.now(),
            )
            for i in range(5)
        ]
        unique = self.fetcher.deduplicate(articles)
        assert len(unique) == 5

    def test_fetch_from_web_invalid_url(self):
        result = self.fetcher.fetch_from_web("https://this-definitely-does-not-exist-12345.com")
        assert result is None


class TestArticleFetcherProperties:
    """Property-based tests for fetcher behavior"""

    def test_content_hash_uniqueness(self):
        """Different content should produce different hashes"""
        articles = [
            RawArticle(
                url=f"https://example.com/{i}",
                title=f"Article {i}",
                content=f"Unique content number {i} that is long enough to pass.",
                source="Test",
                published_date=datetime.now(),
            )
            for i in range(10)
        ]
        hashes = {a.content_hash for a in articles}
        assert len(hashes) == 10

    def test_raw_article_content_hash_generation(self):
        """Content hash should be auto-generated"""
        article = RawArticle(
            url="https://example.com/test",
            title="Test",
            content="Some content here that is reasonable length.",
            source="Test",
            published_date=datetime.now(),
        )
        assert article.content_hash is not None
        assert len(article.content_hash) == 64  # SHA-256 hex digest
