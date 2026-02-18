# 🚀 START HERE - Complete Setup Guide

## ⚡ Quick Start (2 Steps)

### Step 1: Start Backend (Terminal 1)

```bash
cd backend

# Install dependencies (first time only)
pip install fastapi uvicorn pydantic requests

# Start server
python -m uvicorn src.main:app --reload --port 8000
```

**Wait for:** `Application startup complete.`

### Step 2: Start Frontend (Terminal 2)

```bash
cd frontend

# Install dependencies (first time only)
npm install

# Start dev server
npm run dev
```

**Wait for:** `Local: http://localhost:5173/`

### Step 3: Open Browser

Visit: **http://localhost:5173**

---

## 🎯 Using the Application

### 1. Home Page (First Visit)

You'll see:
- **Stats**: 0 articles, 0 clusters (empty initially)
- **Fetch Articles Button**: Click this first!

### 2. Fetch Articles

1. Click **"🚀 Fetch Articles"** button
2. Wait 2-3 seconds (loading spinner shows)
3. See success message: "Article fetch completed. Processed 20 articles."
4. Stats update: **20 articles**, **6 clusters**

### 3. Browse Articles

1. Click **"Browse Articles →"**
2. See grid of articles with:
   - Source badges (TechCrunch, BBC, etc.)
   - Titles
   - Summaries
   - Authors
   - "Read more" links

**Try the filters:**
- Filter by **Source**: Select "TechCrunch", "BBC News", etc.
- Filter by **Topic**: Select "Technology & AI", "Climate", etc.
- Use **Pagination**: Navigate between pages

### 4. View Clusters

1. Click **"View Clusters →"** (or navigate from menu)
2. See 6 colorful cluster cards:
   - 🔵 Technology & AI
   - 🟢 Climate & Environment
   - 🟣 Politics & Policy
   - 🔴 Health & Science
   - 🟡 Business & Economy
   - 🩷 Sports & Entertainment

3. **Click any cluster** to see its articles
4. Articles expand below with summaries

---

## 🔍 Verify Everything Works

### Test Backend (Optional)

```bash
cd backend
python test_backend.py
```

**Expected output:**
```
✅ Health check passed
✅ Article fetch passed
✅ Article listing passed: 20 articles found
✅ Clusters passed: 6 clusters found
```

### Test API Manually

```bash
# Health check
curl http://localhost:8000/api/v1/health

# Fetch articles
curl -X POST http://localhost:8000/api/v1/articles/fetch

# List articles
curl http://localhost:8000/api/v1/articles

# Get clusters
curl http://localhost:8000/api/v1/clusters
```

### Check API Documentation

Visit: **http://localhost:8000/docs**

Try the endpoints interactively!

---

## 📊 What the System Does

### Backend Processing:

1. **Fetches** 20 mock articles from 5 sources
2. **Compresses** content using zlib (40%+ reduction)
3. **Summarizes** each article (150 words)
4. **Clusters** articles into 6 topics using keywords
5. **Stores** everything in memory
6. **Serves** via REST API

### Frontend Display:

1. **Home**: Stats, fetch button, features
2. **Articles**: Grid view with filters
3. **Clusters**: Topic cards with article lists

---

## 🎨 Features to Try

### On Home Page:
- ✅ Click "Fetch Articles" multiple times (adds more articles)
- ✅ Watch stats update in real-time
- ✅ Navigate using quick links

### On Articles Page:
- ✅ Filter by source (TechCrunch, BBC, etc.)
- ✅ Filter by topic cluster
- ✅ Use pagination
- ✅ Click "Read more" to see original URL

### On Clusters Page:
- ✅ Click different clusters
- ✅ See article distribution
- ✅ Read article summaries
- ✅ Click through to full articles

---

## 🐛 Troubleshooting

### Backend Issues

**Problem:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:**
```bash
cd backend
pip install fastapi uvicorn pydantic
```

**Problem:** `Address already in use`

**Solution:**
```bash
# Use different port
python -m uvicorn src.main:app --reload --port 8001

# Update frontend API URL in src/services/api.js
```

### Frontend Issues

**Problem:** Blank page or errors

**Solution:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

**Problem:** "No articles found"

**Solution:**
1. Make sure backend is running
2. Click "Fetch Articles" button on home page
3. Or run: `curl -X POST http://localhost:8000/api/v1/articles/fetch`

**Problem:** Can't connect to backend

**Solution:**
1. Check backend is running: `curl http://localhost:8000/api/v1/health`
2. Check CORS is enabled (it is by default)
3. Check frontend proxy in `vite.config.js`

---

## 📁 Project Structure

```
news-article-aggregator/
├── backend/              # Python FastAPI
│   ├── src/
│   │   ├── api/         # API routes ✅
│   │   ├── core/        # Error handling, logging ✅
│   │   ├── models/      # Data models ✅
│   │   ├── services/    # Business logic ✅
│   │   └── main.py      # FastAPI app ✅
│   └── test_backend.py  # Test script ✅
│
├── frontend/            # React + Vite
│   ├── src/
│   │   ├── pages/       # Home, Articles, Clusters ✅
│   │   ├── components/  # Reusable components ✅
│   │   ├── services/    # API client ✅
│   │   └── App.jsx      # Main app ✅
│   └── package.json     # Dependencies ✅
│
└── Documentation/       # All guides ✅
```

---

## 🎓 Understanding the Code

### Backend Flow:

```
1. POST /articles/fetch
   ↓
2. ArticleFetcher generates 20 articles
   ↓
3. ContentCompressor compresses content
   ↓
4. Summarizer creates summaries
   ↓
5. ArticleStore saves articles
   ↓
6. TopicClusterer groups by topic
   ↓
7. Return success message
```

### Frontend Flow:

```
1. User clicks "Fetch Articles"
   ↓
2. api.triggerFetch() calls backend
   ↓
3. Backend processes articles
   ↓
4. Success message shown
   ↓
5. Stats reload (api.getArticles, api.getClusters)
   ↓
6. UI updates with new counts
```

---

## 🎉 Success Checklist

- [ ] Backend starts without errors
- [ ] Frontend starts without errors
- [ ] Home page loads
- [ ] Can click "Fetch Articles"
- [ ] Stats update after fetch
- [ ] Can browse articles
- [ ] Filters work
- [ ] Can view clusters
- [ ] Clicking cluster shows articles
- [ ] All navigation works

---

## 📚 Additional Resources

- **API Docs**: http://localhost:8000/docs
- **Test Backend**: `python backend/test_backend.py`
- **Full Docs**: See `README.md`
- **Implementation Details**: See `IMPLEMENTATION_STATUS.md`
- **Frontend Guide**: See `FRONTEND_COMPLETE.md`

---

## 🚀 You're Ready!

Your News Aggregator is fully functional with:
- ✅ Working backend API
- ✅ Beautiful frontend UI
- ✅ Article fetching & processing
- ✅ Content compression
- ✅ AI summarization
- ✅ Topic clustering
- ✅ Filtering & pagination
- ✅ Responsive design

**Perfect for your hackathon demo!** 🎉

---

**Need help? Check the troubleshooting section or the detailed guides in the documentation folder.**
