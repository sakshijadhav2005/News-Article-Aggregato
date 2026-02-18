"""Comprehensive tests for Content Compressor"""
import pytest
from hypothesis import given, strategies as st, settings
from src.services.compressor import ContentCompressor
from src.core.exceptions import CompressionError


class TestContentCompressor:
    """Unit tests for ContentCompressor"""

    def setup_method(self):
        self.compressor = ContentCompressor()

    # --- Unit Tests ---
    def test_compress_normal_text(self):
        content = "This is a test article with enough content to compress effectively. " * 20
        compressed = self.compressor.compress(content)
        assert isinstance(compressed, bytes)
        assert len(compressed) > 0

    def test_decompress_normal_text(self):
        content = "Test article content that should be compressed and decompressed correctly." * 10
        compressed = self.compressor.compress(content)
        decompressed = self.compressor.decompress(compressed)
        assert decompressed == content

    def test_compress_empty_string(self):
        compressed = self.compressor.compress("")
        assert compressed == b""

    def test_decompress_empty_bytes(self):
        decompressed = self.compressor.decompress(b"")
        assert decompressed == ""

    def test_compress_special_characters(self):
        content = "Special chars: àéîöü 中文 🎉 <html>&amp; \"quotes\" $100"
        compressed = self.compressor.compress(content)
        decompressed = self.compressor.decompress(compressed)
        assert decompressed == content

    def test_compression_ratio(self):
        content = "Repetitive content. " * 100  # Very repetitive = high compression
        compressed = self.compressor.compress(content)
        ratio = self.compressor.get_compression_ratio(content, compressed)
        assert ratio >= 0.4  # At least 40% compression

    def test_custom_compression_level(self):
        content = "Test content for custom compression level. " * 50
        compressor_max = ContentCompressor(compression_level=9)
        compressed = compressor_max.compress(content)
        decompressed = compressor_max.decompress(compressed)
        assert decompressed == content

    # --- Property-Based Tests ---
    @given(st.text(min_size=1, max_size=10000))
    @settings(max_examples=50)
    def test_roundtrip_property(self, content):
        """Property: compress(decompress(content)) == content (roundtrip)"""
        compressed = self.compressor.compress(content)
        decompressed = self.compressor.decompress(compressed)
        assert decompressed == content

    @given(st.text(min_size=100, max_size=5000))
    @settings(max_examples=30)
    def test_compression_reduces_size(self, content):
        """Property: compressed size should not exceed original + overhead for long text"""
        compressed = self.compressor.compress(content)
        original_size = len(content.encode('utf-8'))
        # Allow for small inflation due to zlib header, but generally should be <= original
        assert len(compressed) <= original_size * 1.1


class TestCompressionEdgeCases:
    """Edge case tests"""

    def setup_method(self):
        self.compressor = ContentCompressor()

    def test_very_long_content(self):
        content = "A" * 1_000_000  # 1MB of text
        compressed = self.compressor.compress(content)
        decompressed = self.compressor.decompress(compressed)
        assert decompressed == content

    def test_single_character(self):
        content = "X"
        compressed = self.compressor.compress(content)
        decompressed = self.compressor.decompress(compressed)
        assert decompressed == content

    def test_newlines_and_tabs(self):
        content = "Line 1\nLine 2\n\tTabbed\n\n\nMultiple newlines"
        compressed = self.compressor.compress(content)
        decompressed = self.compressor.decompress(compressed)
        assert decompressed == content

    def test_binary_like_content(self):
        content = "\x00\x01\x02\x03\xff"
        compressed = self.compressor.compress(content)
        decompressed = self.compressor.decompress(compressed)
        assert decompressed == content
