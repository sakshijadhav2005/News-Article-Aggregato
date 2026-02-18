"""Real cache management service using Redis"""
import logging
import json
import pickle
from typing import Any, Optional, Callable
from datetime import datetime, timedelta
from ..core.exceptions import CacheError
from ..core.error_handler import handle_errors

logger = logging.getLogger(__name__)

# Lazy-loaded Redis client
_redis_client = None


async def _get_redis_client():
    """Get or create async Redis client"""
    global _redis_client

    if _redis_client is not None:
        try:
            await _redis_client.ping()
            return _redis_client
        except Exception:
            _redis_client = None

    try:
        import redis.asyncio as aioredis
        from config.settings import settings

        _redis_client = aioredis.from_url(
            settings.redis.url,
            max_connections=settings.redis.max_connections,
            decode_responses=False,
        )
        await _redis_client.ping()
        logger.info("Redis connection established")
        return _redis_client

    except Exception as e:
        logger.warning(f"Redis not available, using in-memory fallback: {e}")
        return None


async def close_redis():
    """Close Redis connection"""
    global _redis_client
    if _redis_client:
        await _redis_client.close()
        _redis_client = None
        logger.info("Redis connection closed")


class CacheManager:
    """
    Production cache management service.
    Uses Redis when available, falls back to in-memory cache.
    """

    def __init__(self):
        """Initialize cache"""
        self._memory_cache: dict[str, tuple[Any, datetime]] = {}
        self._redis_available = None
        logger.info("CacheManager initialized")

    async def _get_redis(self):
        """Get Redis client if available"""
        if self._redis_available is False:
            return None
        client = await _get_redis_client()
        self._redis_available = client is not None
        return client

    @handle_errors
    async def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache (Redis first, then in-memory fallback).

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found/expired
        """
        redis = await self._get_redis()

        if redis:
            try:
                data = await redis.get(key)
                if data is not None:
                    logger.debug(f"Redis cache hit: {key}")
                    try:
                        return json.loads(data)
                    except (json.JSONDecodeError, TypeError):
                        return pickle.loads(data)
                logger.debug(f"Redis cache miss: {key}")
                return None
            except Exception as e:
                logger.debug(f"Redis get failed: {e}")

        # In-memory fallback
        if key in self._memory_cache:
            value, expiry = self._memory_cache[key]
            if datetime.now() > expiry:
                del self._memory_cache[key]
                logger.debug(f"Memory cache expired: {key}")
                return None
            logger.debug(f"Memory cache hit: {key}")
            return value

        logger.debug(f"Cache miss: {key}")
        return None

    @handle_errors
    async def set(self, key: str, value: Any, ttl: int = 3600) -> None:
        """
        Set value in cache.

        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds (default 1 hour)
        """
        redis = await self._get_redis()

        if redis:
            try:
                try:
                    data = json.dumps(value)
                except (TypeError, ValueError):
                    data = pickle.dumps(value)
                await redis.setex(key, ttl, data)
                logger.debug(f"Redis cache set: {key} (TTL: {ttl}s)")
                return
            except Exception as e:
                logger.debug(f"Redis set failed: {e}")

        # In-memory fallback
        expiry = datetime.now() + timedelta(seconds=ttl)
        self._memory_cache[key] = (value, expiry)
        logger.debug(f"Memory cache set: {key} (TTL: {ttl}s)")

    @handle_errors
    async def delete(self, key: str) -> None:
        """
        Delete value from cache.

        Args:
            key: Cache key
        """
        redis = await self._get_redis()
        if redis:
            try:
                await redis.delete(key)
            except Exception as e:
                logger.debug(f"Redis delete failed: {e}")

        if key in self._memory_cache:
            del self._memory_cache[key]
            logger.debug(f"Cache deleted: {key}")

    @handle_errors
    async def get_or_compute(
        self,
        key: str,
        compute_fn: Callable,
        ttl: int = 3600
    ) -> Any:
        """
        Get value from cache or compute if not found.

        Args:
            key: Cache key
            compute_fn: Function to compute value if not cached (can be async)
            ttl: Time to live in seconds

        Returns:
            Cached or computed value
        """
        value = await self.get(key)
        if value is not None:
            return value

        # Compute value
        logger.debug(f"Computing value for key: {key}")
        import asyncio
        if asyncio.iscoroutinefunction(compute_fn):
            value = await compute_fn()
        else:
            value = compute_fn()

        # Cache it
        await self.set(key, value, ttl)
        return value

    async def clear(self) -> None:
        """Clear all cache"""
        redis = await self._get_redis()
        if redis:
            try:
                await redis.flushdb()
            except Exception as e:
                logger.debug(f"Redis flush failed: {e}")

        self._memory_cache.clear()
        logger.info("Cache cleared")

    async def size(self) -> int:
        """Get cache size"""
        redis = await self._get_redis()
        if redis:
            try:
                return await redis.dbsize()
            except Exception:
                pass
        return len(self._memory_cache)
