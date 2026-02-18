# 🚀 Quick Start Guide

## Get Your News Aggregator Running in 3 Minutes!

### Step 1: Start the Backend (1 minute)

```bash
cd backend

# Install dependencies (first time only)
pip install fastapi uvicorn pydantic

# Run the server
python -m uvicorn src.main:app --reload --port 8000
```

✅ Backend running at: **http://localhost:8000**

### Step 2: Load Sample Data (30 seconds)

Open a new terminal and run:

```bash
# Fetch and process 20 sample articles
curl -X POST http://localhost:8000/api/v1/articles/fetch
```

You should see:
```json
{
  "success": true,
  "message": "Article fetch completed. Processed 20 articles."
}
```

### Step 3: Explore the API (1 minute)

**Option A: Use the Interactive API Docs**
1. Open your browser
2. Go to: **http://localhost:8000/docs**
3. Try the endpoints interactively!

**Option B: Use curl commands**

```bash
# List all articles
curl http://localhost:8000/api/v1/articles

# Get clusters
curl http://localhost:8000/api/v1/clusters

# Filter articles by source
curl "http://localhost:8000/api/v1/articles?source=BBC%20News"

# Get articles in Technology cluster
curl http://localhost:8000/api/v1/clusters/0/articles
```

## 🎯 What You Can Do Now

### 1. View All Articles
```bash
curl http://localhost:8000/api/v1/articles | json_pp
```

### 2. Filter Articles
```bash
# By source
curl "http://localhost:8000/api/v1/articles?source=TechCrunch"

# By page
curl "http://localhost:8000/api/v1/articles?page=2&page_size=5"

# By cluster
curl "http://localhost:8000/api/v1/articles?cluster_id=0"
```

### 3. View Clusters
```bash
curl http://localhost:8000/api/v1/clusters | json_pp
```

Available clusters:
- **0**: Technology & AI
- **1**: Climate & Environment
- **2**: Politics & Policy
- **3**: Health & Science
- **4**: Business & Economy
- **5**: Sports & Entertainment

### 4. Get Article Details
```bash
# First, get an article ID from the list
curl http://localhost:8000/api/v1/articles

# Then get full details (replace {id} with actual ID)
curl http://localhost:8000/api/v1/articles/{id}
```

### 5. Get Articles in a Cluster
```bash
# Get all Technology articles
curl http://localhost:8000/api/v1/clusters/0/articles
```

## 🎨 Start the Frontend (Optional)

```bash
cd frontend

# Install dependencies (first time only)
npm install

# Run dev server
npm run dev
```

Visit: **http://localhost:3000**

## 📊 Sample API Responses

### List Articles Response:
```json
{
  "success": true,
  "data": [
    {
      "id": "abc-123",
      "url": "https://example.com/article-1",
      "title": "AI: Breaking News Story 1",
      "summary": "This is a breaking news story about AI...",
      "source": "TechCrunch",
      "author": "Author 1",
      "published_date": "2024-02-13T10:00:00",
      "fetched_date": "2024-02-13T10:05:00",
      "cluster_id": 0
    }
  ],
  "total": 20,
  "page": 1,
  "page_size": 20,
  "total_pages": 1
}
```

### Clusters Response:
```json
{
  "success": true,
  "data": [
    {
      "id": 0,
      "label": "Technology & AI",
      "article_count": 5,
      "latest_article_date": null
    },
    {
      "id": 1,
      "label": "Climate & Environment",
      "article_count": 3,
      "latest_article_date": null
    }
  ]
}
```

## 🐛 Troubleshooting

### Backend won't start?
```bash
# Make sure you're in the backend directory
cd backend

# Check Python version (need 3.11+)
python --version

# Install missing dependencies
pip install fastapi uvicorn pydantic
```

### No articles showing?
```bash
# Trigger article fetch
curl -X POST http://localhost:8000/api/v1/articles/fetch

# Check if it worked
curl http://localhost:8000/api/v1/articles
```

### Port already in use?
```bash
# Use a different port
python -m uvicorn src.main:app --reload --port 8001

# Then access at http://localhost:8001
```

## 🎓 Next Steps

1. ✅ **Explore the API**: Try all endpoints in the docs
2. ✅ **Check the code**: See how compression, summarization, and clustering work
3. ✅ **Build the frontend**: Implement the UI components
4. ✅ **Add features**: Follow tasks.md for more functionality
5. ✅ **Deploy**: Use Docker Compose for full deployment

## 📚 Useful Links

- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/v1/health
- **Frontend**: http://localhost:3000
- **Implementation Status**: See `IMPLEMENTATION_STATUS.md`
- **Full Documentation**: See `README.md`

---

**🎉 You're all set! Your News Aggregator is running!**

Try the API, explore the code, and build amazing features! 🚀
