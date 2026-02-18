"""Custom exception classes for the application"""


class NewsAggregatorException(Exception):
    """Base exception for all application errors"""
    pass


class ArticleNotFoundError(NewsAggregatorException):
    """Raised when an article is not found"""
    pass


class ValidationError(NewsAggregatorException):
    """Raised when validation fails"""
    pass


class CompressionError(NewsAggregatorException):
    """Raised when compression/decompression fails"""
    pass


class FetchError(NewsAggregatorException):
    """Raised when article fetching fails"""
    pass


class SummarizationError(NewsAggregatorException):
    """Raised when summarization fails"""
    pass


class ClusteringError(NewsAggregatorException):
    """Raised when clustering fails"""
    pass


class DatabaseError(NewsAggregatorException):
    """Raised when database operations fail"""
    pass


class CacheError(NewsAggregatorException):
    """Raised when cache operations fail"""
    pass
