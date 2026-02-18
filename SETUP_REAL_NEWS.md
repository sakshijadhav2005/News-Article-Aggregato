# 📰 Setup Real News Fetching

## Install Required Packages

```bash
cd backend
pip install -r requirements-real.txt
```

This installs:
- `feedparser` - For RSS feeds
- `beautifulsoup4` - For HTML parsing
- `requests` - For HTTP requests
- `lxml` - For XML parsing

## Restart Backend

```bash
python run_simple.py
```

Now when you click "Fetch Articles", it will fetch REAL news from:
- BBC News
- CNN
- The Guardian
- Reuters

## What You'll Get

✅ Real article titles
✅ Real article content
✅ Real URLs (clickable links to actual news sites)
✅ Real publication dates
✅ Real authors

## Test It

1. **Fetch real articles:**
```bash
curl -X POST http://localhost:8000/api/v1/articles/fetch
```

2. **Check the articles:**
```bash
curl http://localhost:8000/api/v1/articles
```

You should see real URLs like:
- `https://www.bbc.com/news/...`
- `https://www.cnn.com/...`
- `https://www.theguardian.com/...`

3. **In the frontend:**
   - Click "Fetch Articles"
   - Browse articles
   - Click "View Original" - it will open the REAL news article!

## Troubleshooting

### If it still shows mock data:
1. Make sure you installed the packages: `pip install -r requirements-real.txt`
2. Restart the backend: `python run_simple.py`
3. Check the logs - you should see "Fetched X articles from RSS"

### If RSS feeds are slow:
- RSS feeds can take 10-30 seconds to fetch
- The app will show a loading spinner
- Be patient on first fetch

### If some feeds fail:
- Some RSS feeds may be temporarily unavailable
- The app will skip failed feeds and continue with others
- Check backend logs for details

## Optional: Add More News Sources

Edit `backend/config/settings.py` and add more RSS feeds:

```python
rss_feeds: List[str] = field(default_factory=lambda: [
    "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
    "https://feeds.bbci.co.uk/news/rss.xml",
    "https://rss.cnn.com/rss/edition.rss",
    "https://www.theguardian.com/world/rss",
    "https://feeds.reuters.com/reuters/topNews",
    # Add your own RSS feeds here!
])
```

## 🎉 Done!

Your app now fetches REAL news articles from major news sources!
