"""Standardized API response classes"""
from typing import Any, Optional, Dict, List
from pydantic import BaseModel, field_validator
from datetime import datetime
import math


class APIResponse(BaseModel):
    """Standard API response wrapper"""
    success: bool = True
    data: Optional[Any] = None
    message: Optional[str] = None
    timestamp: datetime = None

    def __init__(self, **data):
        if 'timestamp' not in data or data['timestamp'] is None:
            data['timestamp'] = datetime.utcnow()
        super().__init__(**data)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class PaginatedResponse(BaseModel):
    """Paginated API response"""
    success: bool = True
    data: List[Any]
    total: int
    page: int
    page_size: int
    total_pages: int = 0
    message: Optional[str] = None
    timestamp: datetime = None

    def __init__(self, **data):
        if 'timestamp' not in data or data['timestamp'] is None:
            data['timestamp'] = datetime.utcnow()
        # Auto-calculate total_pages
        total = data.get('total', 0)
        page_size = data.get('page_size', 20)
        if 'total_pages' not in data or data['total_pages'] == 0:
            data['total_pages'] = max(1, math.ceil(total / page_size)) if page_size > 0 else 1
        super().__init__(**data)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class ErrorResponse(BaseModel):
    """RFC 7807 Problem Details for HTTP APIs"""
    type: str
    title: str
    status: int
    detail: str
    instance: str
    timestamp: datetime = None

    def __init__(self, **data):
        if 'timestamp' not in data or data['timestamp'] is None:
            data['timestamp'] = datetime.utcnow()
        super().__init__(**data)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
