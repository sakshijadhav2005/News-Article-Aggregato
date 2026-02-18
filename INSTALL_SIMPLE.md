# 🚀 Simple Installation (No Database Required)

## Step 1: Install Minimal Python Packages

```bash
cd backend
pip install -r requirements-minimal.txt
```

This installs only:
- FastAPI (web framework)
- Uvicorn (web server)
- Pydantic (data validation)
- python-dotenv (environment variables)

## Step 2: Start Backend

```bash
python run_simple.py
```

You should see:
```
============================================================
Starting News Article Aggregator API (Simple Mode)
============================================================
✓ Skipping database/redis - using in-memory storage
✓ Using mock article generation
✓ Using simple extractive summarization
✓ Using keyword-based clustering
✓ Pipeline initialized successfully
============================================================
✓ Application startup complete
============================================================

🚀 API is ready!
   - API Docs: http://localhost:8000/docs
   - Health Check: http://localhost:8000/api/v1/health
```

## Step 3: Install Frontend Dependencies

Open a NEW terminal:

```bash
cd frontend
npm install
```

## Step 4: Start Frontend

```bash
npm run dev
```

You should see:
```
  VITE v5.0.11  ready in 500 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

## Step 5: Open in Browser

Visit: **http://localhost:5173**

---

## ✅ Verify Everything Works

### Test 1: Backend Health Check
```bash
curl http://localhost:8000/api/v1/health
```

Expected: JSON response with `"status": "healthy"`

### Test 2: Fetch Articles
```bash
curl -X POST http://localhost:8000/api/v1/articles/fetch
```

Expected: `"Fetch complete: 20 articles processed"`

### Test 3: List Articles
```bash
curl http://localhost:8000/api/v1/articles
```

Expected: JSON array with 20 articles

### Test 4: Frontend
1. Open http://localhost:5173
2. Click "Fetch Articles" button
3. See stats update to "20 articles, 6 clusters"
4. Click "Browse Articles" to see the grid

---

## 🎉 Success!

Your News Aggregator is now running with:
- ✅ Backend API on port 8000
- ✅ Frontend UI on port 5173
- ✅ In-memory storage (no database needed)
- ✅ Mock article generation
- ✅ Simple summarization
- ✅ Keyword clustering

---

## 🐛 Troubleshooting

### Error: "pip: command not found"
**Fix:** Install Python from https://www.python.org/downloads/

### Error: "npm: command not found"
**Fix:** Install Node.js from https://nodejs.org/

### Error: "Address already in use"
**Fix:** 
```bash
# Backend - use different port
python run_simple.py  # Edit file to change port

# Frontend - use different port
npm run dev -- --port 3000
```

### Error: "ModuleNotFoundError"
**Fix:** Make sure you're in the backend directory:
```bash
cd backend
pip install -r requirements-minimal.txt
python run_simple.py
```

### Frontend shows "Cannot connect to backend"
**Fix:** 
1. Make sure backend is running (check http://localhost:8000/api/v1/health)
2. Check CORS is enabled (it is by default in run_simple.py)

---

## 📚 What's Next?

Once everything is working:
1. Read `HACKATHON_READY.md` for demo tips
2. Check `START_HERE.md` for feature guide
3. View API docs at http://localhost:8000/docs
4. Explore the code in `backend/src/` and `frontend/src/`

---

## 🔧 Optional: Full Installation

If you want the full features (MongoDB, Redis, ML models):

```bash
cd backend
pip install -r requirements.txt
```

Then start MongoDB and Redis, and use:
```bash
python -m uvicorn src.main:app --reload
```

But for the hackathon demo, the simple mode works perfectly! 🎉
