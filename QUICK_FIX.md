# 🔧 Quick Fix - Run Without MongoDB/Redis

If you're getting errors about MongoDB or Redis connections, use this simplified startup method.

## Option 1: Simple Startup (Recommended)

### Backend
```bash
cd backend
python run_simple.py
```

This bypasses MongoDB/Redis and uses in-memory storage only.

### Frontend
```bash
cd frontend
npm run dev
```

---

## Option 2: Minimal Dependencies

Install only the essential packages:

```bash
cd backend
pip install fastapi uvicorn pydantic requests python-dotenv
```

Then run:
```bash
python run_simple.py
```

---

## Common Errors and Fixes

### Error: "ModuleNotFoundError: No module named 'motor'"
**Fix:** Use `run_simple.py` instead of `main.py`

### Error: "Cannot connect to MongoDB"
**Fix:** Use `run_simple.py` - it skips database initialization

### Error: "Redis connection failed"
**Fix:** Use `run_simple.py` - it uses in-memory caching

### Error: "No module named 'transformers'"
**Fix:** The app works without it - uses simple extractive summarization

### Error: "CORS error in frontend"
**Fix:** Already fixed - CORS now allows `http://localhost:5173`

---

## What Works in Simple Mode

✅ All API endpoints
✅ Article fetching (20 mock articles)
✅ Content compression
✅ Summarization (extractive)
✅ Topic clustering (keyword-based)
✅ Filtering and pagination
✅ Full frontend functionality

❌ Data persistence (articles cleared on restart)
❌ Redis caching (uses in-memory instead)
❌ MongoDB storage (uses in-memory instead)

---

## Verify It's Working

### Test Backend
```bash
curl http://localhost:8000/api/v1/health
```

Expected response:
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    ...
  }
}
```

### Test Frontend
Open: http://localhost:5173

You should see the home page with "Fetch Articles" button.

---

## Full Installation (Optional)

If you want MongoDB and Redis:

### Install MongoDB
- Windows: https://www.mongodb.com/try/download/community
- Mac: `brew install mongodb-community`
- Linux: `sudo apt-get install mongodb`

### Install Redis
- Windows: https://github.com/microsoftarchive/redis/releases
- Mac: `brew install redis`
- Linux: `sudo apt-get install redis-server`

### Start Services
```bash
# MongoDB
mongod

# Redis
redis-server
```

### Then use normal startup
```bash
cd backend
python -m uvicorn src.main:app --reload
```

---

## Still Having Issues?

Please share the exact error message you're seeing, including:
1. The full error traceback
2. Which command you ran
3. Your Python version (`python --version`)

I'll help you fix it immediately!
