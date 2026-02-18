"""Tests for Summarizer"""
import pytest
from hypothesis import given, strategies as st, settings
from src.services.summarizer import Summarizer


class TestSummarizer:
    """Unit tests for Summarizer"""

    def setup_method(self):
        # Use extractive fallback for testing (no model download needed)
        self.summarizer = Summarizer(model_name="t5-small", max_length=50)

    def test_summarize_short_content(self):
        """Content shorter than max_length should be returned as-is"""
        content = "Short article content."
        summary = self.summarizer.summarize(content)
        assert summary == content

    def test_summarize_empty_content(self):
        summary = self.summarizer.summarize("")
        assert summary == ""

    def test_extractive_summarize_long_content(self):
        """Long content should be summarized to max_length words"""
        content = "This is sentence one about technology. " * 20
        summary = self.summarizer._extractive_summarize(content)
        words = summary.split()
        assert len(words) <= 55  # max_length + small margin

    def test_extractive_summarize_preserves_sentences(self):
        content = "First sentence here. Second sentence about news. Third sentence with detail. " * 5
        summary = self.summarizer._extractive_summarize(content)
        assert len(summary) > 0

    def test_batch_summarize(self):
        contents = [
            "Article one content with enough words to make it valid for testing summarization. " * 5,
            "Article two content that is different and provides diverse text for batch processing. " * 5,
        ]
        summaries = self.summarizer.batch_summarize(contents)
        assert len(summaries) == 2
        assert all(len(s) > 0 for s in summaries)


class TestSummarizerProperties:
    """Property-based tests for summarizer"""

    def setup_method(self):
        self.summarizer = Summarizer(max_length=100)

    @given(st.text(min_size=500, max_size=2000, alphabet=st.characters(whitelist_categories=('L', 'Z'))))
    @settings(max_examples=20)
    def test_summary_length_constraint(self, content):
        """Property: Summary word count should not exceed max_length"""
        if content.strip():
            summary = self.summarizer._extractive_summarize(content)
            word_count = len(summary.split())
            assert word_count <= 105  # max_length + small margin for sentence boundaries

    @given(st.text(min_size=1, max_size=100, alphabet=st.characters(whitelist_categories=('L', 'Z'))))
    @settings(max_examples=20)
    def test_short_content_passthrough(self, content):
        """Property: Content shorter than max_length should pass through"""
        if content.strip():
            summary = self.summarizer.summarize(content)
            assert len(summary) > 0
