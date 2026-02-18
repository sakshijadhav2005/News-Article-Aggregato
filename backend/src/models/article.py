"""Article data models"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import hashlib
import numpy as np


@dataclass
class RawArticle:
    """Raw article fetched from external sources"""
    url: str
    title: str
    content: str
    source: str
    published_date: datetime
    author: Optional[str] = None
    content_hash: str = field(init=False)
    
    def __post_init__(self):
        """Generate content hash after initialization"""
        self.content_hash = hashlib.sha256(
            self.content.encode('utf-8')
        ).hexdigest()


@dataclass
class Article:
    """Article stored in database"""
    id: str
    url: str
    title: str
    compressed_content: bytes
    summary: Optional[str]
    source: str
    author: Optional[str]
    published_date: datetime
    fetched_date: datetime
    cluster_id: Optional[int]
    embedding: Optional[np.ndarray] = None
    content_hash: Optional[str] = None
    
    def get_content(self, decompressor) -> str:
        """
        Get decompressed content
        
        Args:
            decompressor: ContentCompressor instance
            
        Returns:
            Decompressed content string
        """
        return decompressor.decompress(self.compressed_content)


@dataclass
class QueryFilters:
    """Filters for querying articles"""
    source: Optional[str] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    cluster_id: Optional[int] = None
    search_text: Optional[str] = None


@dataclass
class Cluster:
    """Topic cluster"""
    id: int
    label: str
    article_ids: list[str]
    centroid: Optional[np.ndarray]
    created_at: datetime
    updated_at: datetime
    article_count: int = field(init=False)
    
    def __post_init__(self):
        """Calculate article count"""
        self.article_count = len(self.article_ids)
