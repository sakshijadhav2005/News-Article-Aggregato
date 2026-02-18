"""Database connection and collection management using async Motor (MongoDB)"""
import logging
from datetime import datetime

from config.settings import settings

logger = logging.getLogger(__name__)

# Motor client and database (initialized lazily)
_client = None
_database = None


async def get_client():
    """Get or create the async MongoDB client"""
    global _client
    if _client is None:
        from motor.motor_asyncio import AsyncIOMotorClient
        _client = AsyncIOMotorClient(settings.database.url)
        logger.info("MongoDB client created")
    return _client


async def get_db():
    """Get the MongoDB database instance"""
    global _database
    if _database is None:
        client = await get_client()
        _database = client[settings.database.db_name]
        logger.info(f"Connected to database: {settings.database.db_name}")
    return _database


async def init_db():
    """Initialize database - create indexes for articles and clusters collections"""
    db = await get_db()

    # Create articles collection indexes
    articles = db["articles"]
    await articles.create_index("url", unique=True)
    await articles.create_index("content_hash", unique=True)
    await articles.create_index("published_date")
    await articles.create_index("source")
    await articles.create_index("cluster_id")

    # Create clusters collection indexes
    clusters = db["clusters"]
    await clusters.create_index("label")

    logger.info("MongoDB indexes created successfully")


async def close_db():
    """Close MongoDB connections"""
    global _client, _database
    if _client:
        _client.close()
        _client = None
        _database = None
        logger.info("MongoDB connections closed")
