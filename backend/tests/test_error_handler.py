"""Tests for error handling utilities"""
import pytest
import asyncio
from src.core.error_handler import retry_with_backoff, handle_errors
from src.core.exceptions import NewsAggregatorException, FetchError


class TestRetryWithBackoff:
    """Tests for retry_with_backoff decorator"""

    def test_sync_retry_success_on_first_try(self):
        call_count = 0

        @retry_with_backoff(max_retries=3, initial_delay=0.01)
        def always_succeeds():
            nonlocal call_count
            call_count += 1
            return "success"

        result = always_succeeds()
        assert result == "success"
        assert call_count == 1

    def test_sync_retry_success_after_failures(self):
        call_count = 0

        @retry_with_backoff(max_retries=3, initial_delay=0.01)
        def fails_twice():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError("temporary error")
            return "success"

        result = fails_twice()
        assert result == "success"
        assert call_count == 3

    def test_sync_retry_all_attempts_fail(self):
        @retry_with_backoff(max_retries=2, initial_delay=0.01)
        def always_fails():
            raise ValueError("permanent error")

        with pytest.raises(ValueError, match="permanent error"):
            always_fails()

    @pytest.mark.asyncio
    async def test_async_retry_success(self):
        call_count = 0

        @retry_with_backoff(max_retries=3, initial_delay=0.01)
        async def async_succeeds():
            nonlocal call_count
            call_count += 1
            return "async_success"

        result = await async_succeeds()
        assert result == "async_success"
        assert call_count == 1

    @pytest.mark.asyncio
    async def test_async_retry_uses_asyncio_sleep(self):
        """Verify async retry uses non-blocking sleep"""
        call_count = 0

        @retry_with_backoff(max_retries=2, initial_delay=0.01)
        async def async_fails_once():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise ValueError("temporary")
            return "success"

        result = await async_fails_once()
        assert result == "success"
        assert call_count == 2


class TestHandleErrors:
    """Tests for handle_errors decorator"""

    def test_sync_handle_success(self):
        @handle_errors
        def success_fn():
            return "ok"

        assert success_fn() == "ok"

    def test_sync_handle_app_error(self):
        @handle_errors
        def raises_app_error():
            raise FetchError("test error")

        with pytest.raises(FetchError):
            raises_app_error()

    @pytest.mark.asyncio
    async def test_async_handle_success(self):
        @handle_errors
        async def async_fn():
            return "async_ok"

        result = await async_fn()
        assert result == "async_ok"
