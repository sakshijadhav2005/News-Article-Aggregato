"""Real article fetching service with RSS, NewsAPI, and web scraping support"""
import logging
import hashlib
import asyncio
from typing import List, Optional, Dict
from datetime import datetime, timedelta
from ..models.article import RawArticle
from ..core.exceptions import FetchError
from ..core.error_handler import handle_errors

logger = logging.getLogger(__name__)

# Optional imports - gracefully handle missing packages
try:
    import aiohttp
    AIOHTTP_AVAILABLE = True
except ImportError:
    AIOHTTP_AVAILABLE = False
    logger.warning("aiohttp not available - async fetching disabled")

try:
    import feedparser
    FEEDPARSER_AVAILABLE = True
except ImportError:
    FEEDPARSER_AVAILABLE = False
    logger.warning("feedparser not available - RSS feeds disabled")

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    logger.warning("requests not available - HTTP fetching disabled")

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False
    logger.warning("beautifulsoup4 not available - HTML parsing disabled")


class ArticleFetcher:
    """
    Production article fetching service.
    Supports RSS feeds, NewsAPI, and web scraping.
    """

    DEFAULT_RSS_FEEDS = [
        "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
        "https://feeds.bbci.co.uk/news/rss.xml",
        "https://rss.cnn.com/rss/edition.rss",
        "https://www.theguardian.com/world/rss",
    ]

    def __init__(self, newsapi_key: str = "", rss_feeds: List[str] = None,
                 timeout: int = 10, max_retries: int = 3, min_content_words: int = 100):
        self.newsapi_key = newsapi_key
        self.rss_feeds = rss_feeds or self.DEFAULT_RSS_FEEDS
        self.timeout = timeout
        self.max_retries = max_retries
        self.min_content_words = min_content_words
        logger.info(f"ArticleFetcher initialized with {len(self.rss_feeds)} RSS feeds")

    @handle_errors
    def fetch_articles(self, count: int = 50) -> List[RawArticle]:
        """
        Fetch articles from all configured sources.

        Args:
            count: Maximum number of articles to fetch

        Returns:
            List of RawArticle objects
        """
        # Check if required libraries are available
        if not FEEDPARSER_AVAILABLE and not REQUESTS_AVAILABLE:
            error_msg = (
                "Cannot fetch real articles - required packages not installed.\n"
                "Please install: pip install feedparser beautifulsoup4 requests lxml"
            )
            logger.error(error_msg)
            raise FetchError(error_msg)
        
        all_articles = []

        # Fetch from RSS feeds
        if FEEDPARSER_AVAILABLE:
            for feed_url in self.rss_feeds:
                try:
                    rss_articles = self._fetch_from_rss(feed_url)
                    all_articles.extend(rss_articles)
                    logger.info(f"Fetched {len(rss_articles)} articles from RSS: {feed_url}")
                except Exception as e:
                    logger.warning(f"Failed to fetch RSS feed {feed_url}: {e}")
                    continue

        # Fetch from NewsAPI if key is available
        if self.newsapi_key and REQUESTS_AVAILABLE:
            try:
                newsapi_articles = self._fetch_from_newsapi()
                all_articles.extend(newsapi_articles)
                logger.info(f"Fetched {len(newsapi_articles)} articles from NewsAPI")
            except Exception as e:
                logger.warning(f"Failed to fetch from NewsAPI: {e}")

        # If no articles fetched, raise error
        if not all_articles:
            error_msg = (
                "No articles could be fetched from any source.\n"
                "Please check:\n"
                "1. Internet connection\n"
                "2. RSS feeds are accessible\n"
                "3. Required packages are installed: pip install feedparser beautifulsoup4 requests lxml"
            )
            logger.error(error_msg)
            raise FetchError(error_msg)

        # Filter short articles
        filtered = [a for a in all_articles if len(a.content.split()) >= self.min_content_words]
        logger.info(f"Filtered {len(all_articles) - len(filtered)} short articles")

        # Deduplicate
        unique = self.deduplicate(filtered)

        # Limit to requested count
        result = unique[:count]
        logger.info(f"Returning {len(result)} REAL articles from news sources")
        return result

    def _fetch_from_rss(self, feed_url: str) -> List[RawArticle]:
        """Fetch articles from an RSS feed"""
        if not FEEDPARSER_AVAILABLE or not BS4_AVAILABLE:
            logger.warning("feedparser or beautifulsoup4 not available - skipping RSS")
            return []
        
        articles = []

        try:
            import feedparser
            from bs4 import BeautifulSoup
            
            feed = feedparser.parse(feed_url)

            if feed.bozo and not feed.entries:
                logger.warning(f"RSS feed error for {feed_url}: {feed.bozo_exception}")
                return articles

            source_name = feed.feed.get("title", feed_url)

            for entry in feed.entries[:20]:  # Limit per feed
                try:
                    title = entry.get("title", "").strip()
                    link = entry.get("link", "")
                    author = entry.get("author", None)

                    # Get published date
                    pub_date = None
                    if hasattr(entry, "published_parsed") and entry.published_parsed:
                        pub_date = datetime(*entry.published_parsed[:6])
                    elif hasattr(entry, "updated_parsed") and entry.updated_parsed:
                        pub_date = datetime(*entry.updated_parsed[:6])
                    else:
                        pub_date = datetime.now()

                    # Get content - try multiple fields
                    content = ""
                    if hasattr(entry, "content") and entry.content:
                        content = entry.content[0].get("value", "")
                    elif hasattr(entry, "summary"):
                        content = entry.get("summary", "")
                    elif hasattr(entry, "description"):
                        content = entry.get("description", "")

                    # Clean HTML from content
                    if content:
                        soup = BeautifulSoup(content, "html.parser")
                        content = soup.get_text(separator=" ", strip=True)

                    # If content is too short, try to fetch the full page
                    if len(content.split()) < self.min_content_words and link:
                        try:
                            full_content = self._scrape_article_content(link)
                            if full_content and len(full_content.split()) > len(content.split()):
                                content = full_content
                        except Exception:
                            pass

                    if not title or not content:
                        continue

                    article = RawArticle(
                        url=link,
                        title=title,
                        content=content,
                        source=source_name,
                        published_date=pub_date,
                        author=author,
                    )
                    articles.append(article)

                except Exception as e:
                    logger.debug(f"Skipping RSS entry: {e}")
                    continue

        except Exception as e:
            raise FetchError(f"RSS fetch failed for {feed_url}: {e}")

        return articles

    def _fetch_from_newsapi(self, query: str = "latest news", page_size: int = 20) -> List[RawArticle]:
        """Fetch articles from NewsAPI"""
        if not REQUESTS_AVAILABLE or not BS4_AVAILABLE:
            logger.warning("requests or beautifulsoup4 not available - skipping NewsAPI")
            return []
        
        articles = []

        try:
            import requests
            from bs4 import BeautifulSoup
            
            url = "https://newsapi.org/v2/everything"
            params = {
                "q": query,
                "pageSize": page_size,
                "sortBy": "publishedAt",
                "language": "en",
                "apiKey": self.newsapi_key,
            }

            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()

            if data.get("status") != "ok":
                logger.warning(f"NewsAPI returned status: {data.get('status')}")
                return articles

            for item in data.get("articles", []):
                try:
                    title = item.get("title", "").strip()
                    content = item.get("content", "") or item.get("description", "") or ""
                    url_str = item.get("url", "")
                    source = item.get("source", {}).get("name", "NewsAPI")
                    author = item.get("author", None)

                    pub_date_str = item.get("publishedAt", "")
                    try:
                        pub_date = datetime.fromisoformat(pub_date_str.replace("Z", "+00:00"))
                        pub_date = pub_date.replace(tzinfo=None)
                    except (ValueError, AttributeError):
                        pub_date = datetime.now()

                    # Clean content
                    if content:
                        soup = BeautifulSoup(content, "html.parser")
                        content = soup.get_text(separator=" ", strip=True)
                        # NewsAPI truncates content - try full scrape
                        if len(content.split()) < self.min_content_words and url_str:
                            try:
                                full_content = self._scrape_article_content(url_str)
                                if full_content and len(full_content.split()) > len(content.split()):
                                    content = full_content
                            except Exception:
                                pass

                    if not title or not content:
                        continue

                    article = RawArticle(
                        url=url_str,
                        title=title,
                        content=content,
                        source=source,
                        published_date=pub_date,
                        author=author,
                    )
                    articles.append(article)

                except Exception as e:
                    logger.debug(f"Skipping NewsAPI article: {e}")
                    continue

        except requests.RequestException as e:
            raise FetchError(f"NewsAPI fetch failed: {e}")

        return articles

    def _scrape_article_content(self, url: str) -> str:
        """Scrape article content from a URL using BeautifulSoup"""
        if not REQUESTS_AVAILABLE or not BS4_AVAILABLE:
            return ""
        
        try:
            import requests
            from bs4 import BeautifulSoup
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            response = requests.get(url, headers=headers, timeout=self.timeout)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            # Remove script and style elements
            for element in soup(["script", "style", "nav", "header", "footer", "aside"]):
                element.decompose()

            # Try to find article content in common containers
            article = soup.find("article") or soup.find("main")
            if article:
                paragraphs = article.find_all("p")
            else:
                paragraphs = soup.find_all("p")

            text_parts = []
            for p in paragraphs:
                text = p.get_text(strip=True)
                if len(text) > 30:  # Skip very short paragraphs
                    text_parts.append(text)

            return " ".join(text_parts)

        except Exception as e:
            logger.debug(f"Web scraping failed for {url}: {e}")
            return ""

    @handle_errors
    def deduplicate(self, articles: List[RawArticle]) -> List[RawArticle]:
        """
        Remove duplicate articles based on URL and content hash.

        Args:
            articles: List of articles

        Returns:
            Deduplicated list
        """
        seen_hashes = set()
        seen_urls = set()
        unique_articles = []

        for article in articles:
            if article.content_hash in seen_hashes or article.url in seen_urls:
                logger.debug(f"Duplicate article found: {article.title}")
                continue

            seen_hashes.add(article.content_hash)
            seen_urls.add(article.url)
            unique_articles.append(article)

        logger.info(f"Deduplicated {len(articles)} to {len(unique_articles)} articles")
        return unique_articles

    def fetch_from_web(self, url: str) -> Optional[RawArticle]:
        """
        Fetch a single article from a web URL.

        Args:
            url: Article URL

        Returns:
            RawArticle or None
        """
        try:
            content = self._scrape_article_content(url)
            if not content:
                return None

            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers, timeout=self.timeout)
            soup = BeautifulSoup(response.text, "html.parser")

            title = ""
            title_tag = soup.find("title")
            if title_tag:
                title = title_tag.get_text(strip=True)

            og_title = soup.find("meta", property="og:title")
            if og_title:
                title = og_title.get("content", title)

            if not title:
                title = "Untitled Article"

            return RawArticle(
                url=url,
                title=title,
                content=content,
                source=url.split("/")[2] if "/" in url else "Web",
                published_date=datetime.now(),
                author=None,
            )

        except Exception as e:
            logger.error(f"Failed to fetch article from {url}: {e}")
            return None
