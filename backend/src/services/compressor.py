"""Content compression service using zlib"""
import zlib
import logging
from typing import Optional
from ..core.exceptions import CompressionError
from ..core.error_handler import handle_errors

logger = logging.getLogger(__name__)


class ContentCompressor:
    """
    Handles compression and decompression of article content
    Uses zlib compression (level 6 for balance of speed and ratio)
    """
    
    def __init__(self, compression_level: int = 6):
        """
        Initialize compressor
        
        Args:
            compression_level: Compression level (0-9, default 6)
        """
        self.compression_level = compression_level
        logger.info(f"ContentCompressor initialized with level {compression_level}")
    
    @handle_errors
    def compress(self, content: str) -> bytes:
        """
        Compress text content
        
        Args:
            content: Text content to compress
            
        Returns:
            Compressed bytes
            
        Raises:
            CompressionError: If compression fails
        """
        if not content:
            logger.warning("Attempting to compress empty content")
            return b""
        
        try:
            # Encode to UTF-8 bytes
            content_bytes = content.encode('utf-8')
            
            # Compress
            compressed = zlib.compress(content_bytes, level=self.compression_level)
            
            # Calculate compression ratio
            ratio = self.get_compression_ratio(content, compressed)
            logger.debug(f"Compressed {len(content_bytes)} bytes to {len(compressed)} bytes (ratio: {ratio:.2%})")
            
            # If compression increases size, return original
            if len(compressed) >= len(content_bytes):
                logger.warning("Compression increased size, returning original")
                return content_bytes
            
            return compressed
            
        except Exception as e:
            logger.error(f"Compression failed: {str(e)}")
            raise CompressionError(f"Failed to compress content: {str(e)}")
    
    @handle_errors
    def decompress(self, compressed: bytes) -> str:
        """
        Decompress content
        
        Args:
            compressed: Compressed bytes
            
        Returns:
            Decompressed text content
            
        Raises:
            CompressionError: If decompression fails
        """
        if not compressed:
            return ""
        
        try:
            # Try to decompress
            try:
                decompressed_bytes = zlib.decompress(compressed)
            except zlib.error:
                # If decompression fails, assume it's uncompressed
                logger.debug("Content appears to be uncompressed")
                decompressed_bytes = compressed
            
            # Decode from UTF-8
            content = decompressed_bytes.decode('utf-8')
            
            logger.debug(f"Decompressed {len(compressed)} bytes to {len(content)} characters")
            
            return content
            
        except Exception as e:
            logger.error(f"Decompression failed: {str(e)}")
            raise CompressionError(f"Failed to decompress content: {str(e)}")
    
    def get_compression_ratio(self, original: str, compressed: bytes) -> float:
        """
        Calculate compression ratio
        
        Args:
            original: Original text content
            compressed: Compressed bytes
            
        Returns:
            Compression ratio (0.0 to 1.0)
        """
        original_size = len(original.encode('utf-8'))
        compressed_size = len(compressed)
        
        if original_size == 0:
            return 0.0
        
        return 1.0 - (compressed_size / original_size)
