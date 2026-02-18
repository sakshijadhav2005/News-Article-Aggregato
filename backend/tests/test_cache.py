"""Tests for Cache Manager (in-memory mode)"""
import pytest
import asyncio
from src.services.cache import CacheManager


@pytest.fixture
def cache():
    cm = CacheManager()
    cm._redis_available = False  # Force in-memory mode
    return cm


class TestCacheManager:
    """Unit tests for CacheManager"""

    @pytest.mark.asyncio
    async def test_set_and_get(self, cache):
        await cache.set("key1", {"data": "value"}, ttl=3600)
        result = await cache.get("key1")
        assert result == {"data": "value"}

    @pytest.mark.asyncio
    async def test_get_nonexistent_key(self, cache):
        result = await cache.get("nonexistent")
        assert result is None

    @pytest.mark.asyncio
    async def test_delete(self, cache):
        await cache.set("key1", "value1")
        await cache.delete("key1")
        result = await cache.get("key1")
        assert result is None

    @pytest.mark.asyncio
    async def test_get_or_compute(self, cache):
        computed_value = {"computed": True}

        def compute():
            return computed_value

        result = await cache.get_or_compute("computed_key", compute, ttl=3600)
        assert result == computed_value

        # Second call should return cached value
        result2 = await cache.get_or_compute("computed_key", compute, ttl=3600)
        assert result2 == computed_value

    @pytest.mark.asyncio
    async def test_clear(self, cache):
        await cache.set("key1", "value1")
        await cache.set("key2", "value2")
        await cache.clear()

        assert await cache.get("key1") is None
        assert await cache.get("key2") is None

    @pytest.mark.asyncio
    async def test_size(self, cache):
        assert await cache.size() == 0
        await cache.set("key1", "value1")
        assert await cache.size() == 1

    @pytest.mark.asyncio
    async def test_different_value_types(self, cache):
        # String
        await cache.set("str", "hello")
        assert await cache.get("str") == "hello"

        # List
        await cache.set("list", [1, 2, 3])
        assert await cache.get("list") == [1, 2, 3]

        # Dict
        await cache.set("dict", {"a": 1, "b": 2})
        assert await cache.get("dict") == {"a": 1, "b": 2}

        # Number
        await cache.set("num", 42)
        assert await cache.get("num") == 42
