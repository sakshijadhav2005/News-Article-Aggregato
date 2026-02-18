"""Application settings loaded from environment variables"""
import os
from dataclasses import dataclass, field
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv()


@dataclass
class DatabaseSettings:
    url: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    db_name: str = os.getenv("MONGODB_DB_NAME", "news_aggregator")


@dataclass
class RedisSettings:
    url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    max_connections: int = int(os.getenv("REDIS_MAX_CONNECTIONS", "20"))
    article_ttl: int = 3600       # 1 hour
    summary_ttl: int = 3600       # 1 hour
    cluster_ttl: int = 1800       # 30 minutes
    query_ttl: int = 900          # 15 minutes


@dataclass
class FetcherSettings:
    newsapi_key: str = os.getenv("NEWSAPI_KEY", "")
    rss_feeds: List[str] = field(default_factory=lambda: [
        "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
        "https://feeds.bbci.co.uk/news/rss.xml",
        "https://rss.cnn.com/rss/edition.rss",
        "https://www.theguardian.com/world/rss",
        "https://feeds.reuters.com/reuters/topNews",
    ])
    rate_limit: int = 10           # requests per second per source
    timeout: int = 10              # seconds
    max_retries: int = 3
    min_content_words: int = 100   # filter out short articles
    fetch_interval_minutes: int = int(os.getenv("FETCH_INTERVAL", "15"))


@dataclass
class SummarizerSettings:
    model_name: str = os.getenv("SUMMARIZER_MODEL", "t5-small")
    max_summary_words: int = 150
    max_input_tokens: int = 512
    num_beams: int = 4
    batch_size: int = 8
    use_gpu: bool = os.getenv("USE_GPU", "false").lower() == "true"


@dataclass
class ClustererSettings:
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    min_cluster_size: int = 5
    min_samples: int = 3
    max_cluster_articles: int = 50
    similarity_threshold: float = 0.7
    recluster_interval_minutes: int = 60


@dataclass
class APISettings:
    host: str = os.getenv("API_HOST", "0.0.0.0")
    port: int = int(os.getenv("API_PORT", "8000"))
    cors_origins: List[str] = field(default_factory=lambda: os.getenv(
        "CORS_ORIGINS", "http://localhost:3000,http://localhost:5173,http://localhost"
    ).split(","))
    rate_limit: str = os.getenv("RATE_LIMIT", "100/minute")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")


@dataclass
class Settings:
    database: DatabaseSettings = field(default_factory=DatabaseSettings)
    redis: RedisSettings = field(default_factory=RedisSettings)
    fetcher: FetcherSettings = field(default_factory=FetcherSettings)
    summarizer: SummarizerSettings = field(default_factory=SummarizerSettings)
    clusterer: ClustererSettings = field(default_factory=ClustererSettings)
    api: APISettings = field(default_factory=APISettings)


# Global settings instance
settings = Settings()
