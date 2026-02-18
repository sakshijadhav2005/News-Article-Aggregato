"""Tests for Topic Clusterer"""
import pytest
from datetime import datetime
import uuid
from src.services.clusterer import TopicClusterer
from src.models.article import Article


def _make_article(title, cluster_id=None):
    """Helper to create test articles"""
    return Article(
        id=str(uuid.uuid4()),
        url=f"https://example.com/{uuid.uuid4()}",
        title=title,
        compressed_content=b"",
        summary=None,
        source="Test Source",
        author="Test Author",
        published_date=datetime.now(),
        fetched_date=datetime.now(),
        cluster_id=cluster_id,
    )


class TestTopicClusterer:
    """Unit tests for TopicClusterer"""

    def setup_method(self):
        self.clusterer = TopicClusterer(min_cluster_size=2, min_samples=2)

    def test_keyword_clustering(self):
        articles = [
            _make_article("New AI technology breakthrough in machine learning"),
            _make_article("Tech company releases new software product"),
            _make_article("Climate change effects on global warming"),
            _make_article("Environmental policy and green energy"),
            _make_article("Sports team wins championship game"),
        ]
        clusters = self.clusterer._keyword_cluster(articles)
        assert len(clusters) > 0
        # Every article should be assigned
        all_ids = set()
        for article_ids in clusters.values():
            all_ids.update(article_ids)
        assert len(all_ids) == 5

    def test_cluster_labels_generated(self):
        articles = [
            _make_article("Technology innovation in the digital world"),
            _make_article("New AI breakthrough announced today"),
        ]
        self.clusterer._keyword_cluster(articles)
        clusters = self.clusterer.get_all_clusters()
        for c in clusters:
            assert c.label is not None
            assert len(c.label) > 0

    def test_get_cluster_not_found(self):
        assert self.clusterer.get_cluster(9999) is None

    def test_empty_articles(self):
        result = self.clusterer.cluster_articles([])
        assert result == {}


class TestTopicClustererProperties:
    """Property-based tests for clusterer behavior"""

    def setup_method(self):
        self.clusterer = TopicClusterer(min_cluster_size=2, min_samples=2)

    def test_all_articles_assigned(self):
        """Property: Every article should be assigned to a cluster"""
        articles = [
            _make_article(f"Article about topic {i} with keyword technology")
            for i in range(10)
        ]
        clusters = self.clusterer._keyword_cluster(articles)

        assigned_ids = set()
        for article_ids in clusters.values():
            assigned_ids.update(article_ids)

        article_ids = {a.id for a in articles}
        assert assigned_ids == article_ids

    def test_cluster_article_count_correct(self):
        """Property: Cluster article_count matches actual article_ids length"""
        articles = [
            _make_article(f"Article {i} about global politics")
            for i in range(5)
        ]
        self.clusterer._keyword_cluster(articles)
        for cluster in self.clusterer.get_all_clusters():
            assert cluster.article_count == len(cluster.article_ids)
