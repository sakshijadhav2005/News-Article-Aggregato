# 🔍 Backend Connectivity Test Guide

## Step 1: Start the Backend

```bash
cd backend
python -m uvicorn src.main:app --reload --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

## Step 2: Test Backend Endpoints

### Test 1: Health Check
```bash
curl http://localhost:8000/api/v1/health
```

**Expected Response:**
```json
{
  "success": true,
  "data": {"status": "healthy"},
  "message": "Service is running",
  "timestamp": "2024-02-14T..."
}
```

### Test 2: Fetch Articles
```bash
curl -X POST http://localhost:8000/api/v1/articles/fetch
```

**Expected Response:**
```json
{
  "success": true,
  "message": "Article fetch completed. Processed 20 articles.",
  "timestamp": "2024-02-14T..."
}
```

### Test 3: List Articles
```bash
curl http://localhost:8000/api/v1/articles
```

**Expected Response:**
```json
{
  "success": true,
  "data": [...],
  "total": 20,
  "page": 1,
  "page_size": 20,
  "total_pages": 1,
  "timestamp": "2024-02-14T..."
}
```

### Test 4: Get Clusters
```bash
curl http://localhost:8000/api/v1/clusters
```

**Expected Response:**
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
    ...
  ],
  "message": "Clusters retrieved successfully",
  "timestamp": "2024-02-14T..."
}
```

## Step 3: Test Frontend Connection

### Start Frontend
```bash
cd frontend
npm run dev
```

**Expected Output:**
```
VITE v5.0.11  ready in 500 ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
➜  press h + enter to show help
```

### Open Browser
Visit: **http://localhost:5173** (or the port shown)

## Step 4: Test Full Flow

1. **Home Page Loads**
   - ✅ See "News Article Aggregator" title
   - ✅ See stats cards (0 articles, 0 clusters initially)
   - ✅ See "Fetch Articles" button

2. **Click "Fetch Articles"**
   - ✅ Button shows loading spinner
   - ✅ Success message appears
   - ✅ Stats update (20 articles, 6 clusters)

3. **Click "Browse Articles"**
   - ✅ Navigate to /articles
   - ✅ See grid of 12 articles
   - ✅ Filters work (source, cluster)
   - ✅ Pagination works

4. **Click "View Clusters"**
   - ✅ Navigate to /clusters
   - ✅ See 6 colorful cluster cards
   - ✅ Click cluster shows articles
   - ✅ Article links work

## 🐛 Troubleshooting

### Issue: Backend won't start

**Error:** `ModuleNotFoundError: No module named 'fastapi'`

**Fix:**
```bash
cd backend
pip install fastapi uvicorn pydantic
```

### Issue: Frontend can't connect to backend

**Error:** `Network Error` or `CORS error`

**Check:**
1. Backend is running on port 8000
2. Frontend proxy is configured in `vite.config.js`
3. CORS is enabled in backend

**Fix:**
```bash
# Check backend is running
curl http://localhost:8000/api/v1/health

# If not, start it
cd backend
python -m uvicorn src.main:app --reload --port 8000
```

### Issue: Frontend shows blank page

**Check browser console (F12)**

**Common fixes:**
```bash
cd frontend

# Clear and reinstall
rm -rf node_modules package-lock.json
npm install

# Restart dev server
npm run dev
```

### Issue: "No articles found"

**Fix:**
```bash
# Fetch articles via API
curl -X POST http://localhost:8000/api/v1/articles/fetch

# Or click "Fetch Articles" button on home page
```

## ✅ Success Checklist

- [ ] Backend starts without errors
- [ ] Health check returns 200 OK
- [ ] Can fetch articles (POST /articles/fetch)
- [ ] Can list articles (GET /articles)
- [ ] Can get clusters (GET /clusters)
- [ ] Frontend loads home page
- [ ] Fetch button works
- [ ] Stats update after fetch
- [ ] Articles page shows articles
- [ ] Filters work
- [ ] Clusters page shows clusters
- [ ] Clicking cluster shows articles

## 🎯 Quick Test Script

Run this to test everything:

```bash
# Test backend
echo "Testing backend..."
curl -s http://localhost:8000/api/v1/health | grep "healthy" && echo "✅ Backend is healthy"

# Fetch articles
echo "Fetching articles..."
curl -s -X POST http://localhost:8000/api/v1/articles/fetch | grep "success" && echo "✅ Articles fetched"

# List articles
echo "Listing articles..."
curl -s http://localhost:8000/api/v1/articles | grep "total" && echo "✅ Articles listed"

# Get clusters
echo "Getting clusters..."
curl -s http://localhost:8000/api/v1/clusters | grep "label" && echo "✅ Clusters retrieved"

echo ""
echo "🎉 All tests passed! Backend is working!"
echo "Now open http://localhost:5173 in your browser"
```

## 📊 Expected Behavior

### After Fetching Articles:

**Backend generates:**
- 20 articles with realistic content
- 6 topic clusters
- Compressed content
- Auto-generated summaries

**Frontend displays:**
- Home: Stats show 20 articles, 6 clusters
- Articles: Grid of 12 articles (paginated)
- Clusters: 6 colorful cluster cards

### Article Distribution:
- Technology & AI: ~3-5 articles
- Climate & Environment: ~2-4 articles
- Politics & Policy: ~2-4 articles
- Health & Science: ~2-4 articles
- Business & Economy: ~2-4 articles
- Sports & Entertainment: ~2-4 articles

---

**Everything should work perfectly! If you encounter any issues, follow the troubleshooting steps above.** 🚀
