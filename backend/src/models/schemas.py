"""Pydantic schemas for API request/response validation"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ArticleResponse(BaseModel):
    """Article response schema"""
    id: str
    title: str
    summary: str = ""
    content: str = ""
    source: str
    author: Optional[str] = None
    published_date: Optional[str] = None
    fetched_date: Optional[str] = None
    url: str
    cluster_id: Optional[int] = None


class ClusterResponse(BaseModel):
    """Cluster response schema"""
    id: int
    label: str
    article_count: int = 0
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class FetchRequest(BaseModel):
    """Request body for manual fetch"""
    count: int = Field(default=20, ge=1, le=100, description="Number of articles to fetch")


class FetchResponse(BaseModel):
    """Response for manual fetch"""
    fetched: int = 0
    stored: int = 0
    summarized: int = 0
    clustered: int = 0
    errors: List[str] = []


class StatsResponse(BaseModel):
    """System statistics"""
    total_articles: int = 0
    total_clusters: int = 0
    cache_size: int = 0
    sources: List[str] = []
