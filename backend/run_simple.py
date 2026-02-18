"""
Simple startup script that bypasses database/redis initialization
Use this if you don't have MongoDB or Redis installed
"""
import sys
import os

# Ensure config is importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
import logging

from src.api.routes import router
from src.api.responses import ErrorResponse
from src.core.logger import setup_logger
from src.core.exceptions import NewsAggregatorException

# Setup logger
logger = setup_logger(name="news_aggregator", level="INFO")

# Global pipeline instance
_pipeline = None


def get_pipeline():
    """Get or create the global pipeline instance"""
    global _pipeline
    if _pipeline is None:
        from src.services.pipeline import Pipeline
        _pipeline = Pipeline()
    return _pipeline


# Create FastAPI app (no lifespan for simplicity)
app = FastAPI(
    title="News Article Aggregator API",
    description="API for news article aggregation, summarization, and clustering",
    version="1.0.0",
)

# Add CORS middleware
from config.settings import settings

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add Gzip compression middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)


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


@app.on_event("startup")
async def startup_event():
    """Startup event - initialize pipeline"""
    logger.info("=" * 60)
    logger.info("Starting News Article Aggregator API (Simple Mode)")
    logger.info("=" * 60)
    logger.info("✓ Skipping database/redis - using in-memory storage")
    logger.info("✓ Using mock article generation")
    logger.info("✓ Using simple extractive summarization")
    logger.info("✓ Using keyword-based clustering")
    
    try:
        # Initialize pipeline
        pipeline = get_pipeline()
        logger.info("✓ Pipeline initialized successfully")
    except Exception as e:
        logger.error(f"✗ Pipeline initialization failed: {e}")
        logger.info("  Continuing anyway - pipeline will initialize on first request")
    
    logger.info("=" * 60)
    logger.info("✓ Application startup complete")
    logger.info("=" * 60)
    logger.info("")
    logger.info("🚀 API is ready!")
    logger.info("   - API Docs: http://localhost:8000/docs")
    logger.info("   - Health Check: http://localhost:8000/api/v1/health")
    logger.info("")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "run_simple:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
