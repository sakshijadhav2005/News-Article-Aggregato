"""Global error handling utilities"""
import functools
import asyncio
import time
import logging
from typing import Callable, Any
from .exceptions import NewsAggregatorException

logger = logging.getLogger(__name__)


def retry_with_backoff(
    max_retries: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0,
    exceptions: tuple = (Exception,)
):
    """
    Decorator for retrying functions with exponential backoff.

    Args:
        max_retries: Maximum number of retry attempts
        initial_delay: Initial delay in seconds
        backoff_factor: Multiplier for delay after each retry
        exceptions: Tuple of exceptions to catch and retry
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs) -> Any:
            delay = initial_delay
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_retries:
                        logger.warning(
                            f"Attempt {attempt + 1}/{max_retries} failed for {func.__name__}: {str(e)}. "
                            f"Retrying in {delay}s..."
                        )
                        await asyncio.sleep(delay)  # Non-blocking async sleep
                        delay *= backoff_factor
                    else:
                        logger.error(
                            f"All {max_retries} retry attempts failed for {func.__name__}: {str(e)}"
                        )

            raise last_exception

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs) -> Any:
            delay = initial_delay
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_retries:
                        logger.warning(
                            f"Attempt {attempt + 1}/{max_retries} failed for {func.__name__}: {str(e)}. "
                            f"Retrying in {delay}s..."
                        )
                        time.sleep(delay)
                        delay *= backoff_factor
                    else:
                        logger.error(
                            f"All {max_retries} retry attempts failed for {func.__name__}: {str(e)}"
                        )

            raise last_exception

        # Return appropriate wrapper based on function type
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator


def handle_errors(func: Callable) -> Callable:
    """
    Decorator for standardized error handling and logging.
    Supports both sync and async functions.
    """
    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs) -> Any:
        try:
            return await func(*args, **kwargs)
        except NewsAggregatorException as e:
            logger.error(f"Application error in {func.__name__}: {str(e)}", exc_info=True)
            raise
        except Exception as e:
            logger.error(f"Unexpected error in {func.__name__}: {str(e)}", exc_info=True)
            raise

    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except NewsAggregatorException as e:
            logger.error(f"Application error in {func.__name__}: {str(e)}", exc_info=True)
            raise
        except Exception as e:
            logger.error(f"Unexpected error in {func.__name__}: {str(e)}", exc_info=True)
            raise

    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper
