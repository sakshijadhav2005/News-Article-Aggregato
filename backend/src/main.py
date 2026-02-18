"""Main FastAPI application with async handlers, lifecycle management, and rate limiting"""
import sys
import os

# Ensure config is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging

from .api.routes import router
from .api.responses import ErrorResponse
from .core.logger import setup_logger
from .core.exceptions import NewsAggregatorException

# Setup logger
logger = setup_logger(name="news_aggregator", level="INFO")

# Global pipeline instance
_pipeline = None


def get_pipeline():
    """Get or create the global pipeline instance"""
    global _pipeline
    if _pipeline is None:
        from .services.pipeline import Pipeline
        _pipeline = Pipeline()
    return _pipeline


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    # ---- STARTUP ----
    logger.info("Starting News Article Aggregator API")

    # Initialize database
    try:
        from .db import init_db
        await init_db()
        logger.info("Database initialized")
    except Exception as e:
        logger.warning(f"Database initialization failed (will use in-memory): {e}")

    # Initialize pipeline (lazy-loads ML models on first use)
    pipeline = get_pipeline()
    logger.info("Pipeline initialized")

    # Run initial article fetch in background
    import asyncio

    async def initial_fetch():
        try:
            await asyncio.sleep(2)  # Give the server time to start
            results = await pipeline.process_articles(count=20)
            logger.info(f"Initial fetch complete: {results}")
        except Exception as e:
            logger.warning(f"Initial fetch failed: {e}")

    asyncio.create_task(initial_fetch())

    logger.info("Application startup complete")

    yield

    # ---- SHUTDOWN ----
    logger.info("Shutting down News Article Aggregator API")

    # Close database connections
    try:
        from .db import close_db
        await close_db()
    except Exception as e:
        logger.warning(f"DB close error: {e}")

    # Close Redis connections
    try:
        from .services.cache import close_redis
        await close_redis()
    except Exception as e:
        logger.warning(f"Redis close error: {e}")

    logger.info("Application shutdown complete")


# Create FastAPI app
app = FastAPI(
    title="News Article Aggregator API",
    description="API for news article aggregation, summarization, and clustering",
    version="1.0.0",
    lifespan=lifespan,
)

# Add CORS middleware
from config.settings import settings

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.api.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add Gzip compression middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Rate limiting
try:
    from slowapi import Limiter, _rate_limit_exceeded_handler
    from slowapi.util import get_remote_address
    from slowapi.errors import RateLimitExceeded

    limiter = Limiter(key_func=get_remote_address)
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    logger.info(f"Rate limiting enabled: {settings.api.rate_limit}")
except ImportError:
    logger.warning("slowapi not installed, rate limiting disabled")


# Global exception handlers
@app.exception_handler(NewsAggregatorException)
async def application_exception_handler(request: Request, exc: NewsAggregatorException):
    """Handle application-specific exceptions"""
    logger.error(f"Application error: {str(exc)}", exc_info=True)

    error_response = ErrorResponse(
        type="https://api.newsaggregator.com/errors/application-error",
        title="Application Error",
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=str(exc),
        instance=str(request.url)
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response.dict()
    )


@app.exception_handler(ValueError)
async def validation_exception_handler(request: Request, exc: ValueError):
    """Handle validation errors"""
    logger.warning(f"Validation error: {str(exc)}")

    error_response = ErrorResponse(
        type="https://api.newsaggregator.com/errors/validation-error",
        title="Validation Error",
        status=status.HTTP_400_BAD_REQUEST,
        detail=str(exc),
        instance=str(request.url)
    )

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=error_response.dict()
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions"""
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)

    error_response = ErrorResponse(
        type="https://api.newsaggregator.com/errors/internal-error",
        title="Internal Server Error",
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="An unexpected error occurred",
        instance=str(request.url)
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response.dict()
    )


# Include API routes
app.include_router(router, prefix="/api/v1", tags=["articles"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "News Article Aggregator API",
        "version": "1.0.0",
        "docs": "/docs",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host=settings.api.host,
        port=settings.api.port,
        reload=True,
        log_level=settings.api.log_level.lower(),
    )
