# Getting Started - News Article Aggregator

## 🎉 Welcome!

Your production-level project structure is ready! This guide will help you start implementing the features.

## ✅ What's Already Done

### Backend Structure
- ✅ FastAPI application with async handlers
- ✅ Standardized API response classes (APIResponse, PaginatedResponse, ErrorResponse)
- ✅ Global error handling with RFC 7807 format
- ✅ Structured JSON logging with context manager
- ✅ Retry decorator with exponential backoff
- ✅ Custom exception hierarchy
- ✅ API routes skeleton with proper error handling
- ✅ Docker configuration
- ✅ Environment variables template

### Frontend Structure
- ✅ React + Vite setup
- ✅ Tailwind CSS with dark mode
- ✅ Error Boundary component
- ✅ Loading Spinner component
- ✅ API service with Axios interceptors
- ✅ React Router setup
- ✅ Docker + Nginx configuration

### DevOps
- ✅ Docker Compose with PostgreSQL, Redis, Backend, Frontend
- ✅ Health checks for all services
- ✅ Volume persistence
- ✅ Nginx reverse proxy

### Documentation
- ✅ Comprehensive requirements (EARS format)
- ✅ Technical design with 23 correctness properties
- ✅ Implementation task list (16 major tasks)
- ✅ README with setup instructions
- ✅ Project structure documentation

## 🚀 Quick Start

### 1. Start the Development Environment

```bash
# Start all services with Docker Compose
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

**Access Points:**
- Frontend: http://localhost
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- PostgreSQL: localhost:5432
- Redis: localhost:6379

### 2. Local Development (Without Docker)

#### Backend
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Run development server
uvicorn src.main:app --reload --port 8000
```

#### Frontend
```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

## 📋 Implementation Workflow

Follow the tasks in `.kiro/specs/news-article-aggregator/tasks.md`:

### Phase 1: Core Components (Tasks 2-4)
1. **Content Compressor** - Implement zlib compression with round-trip testing
2. **Data Models** - Create Article, RawArticle, Cluster dataclasses
3. **Article Store** - PostgreSQL storage with connection pooling
4. **Checkpoint** - Ensure all storage tests pass

### Phase 2: Processing Layer (Tasks 5-8)
5. **Article Fetcher** - RSS, NewsAPI, web scraping with deduplication
6. **Summarizer** - T5-based summarization with error fallback
7. **Topic Clusterer** - HDBSCAN clustering with semantic embeddings
8. **Checkpoint** - Ensure all processing tests pass

### Phase 3: API & Caching (Tasks 9-11)
9. **Cache Manager** - Redis caching with LRU eviction
10. **Error Handling** - Already implemented ✅
11. **API Gateway** - Complete the route implementations

### Phase 4: Integration (Tasks 12-13)
12. **Content Filtering** - Minimum length validation
13. **Pipeline Integration** - Wire all components together

### Phase 5: Frontend (Task 14)
14. **React Components** - Article list, detail view, clusters view

### Phase 6: Deployment (Tasks 15-16)
15. **Configuration** - Environment management
16. **Documentation** - API docs and README

## 🧪 Testing Strategy

### Run Tests
```bash
cd backend

# All tests
pytest

# Unit tests only
pytest -m unit

# Property-based tests only
pytest -m property

# With coverage
pytest --cov=src --cov-report=html
```

### Writing Tests

**Unit Test Example:**
```python
# tests/unit/test_compressor.py
def test_compress_empty_string():
    compressor = ContentCompressor()
    result = compressor.compress("")
    assert result is not None
```

**Property Test Example:**
```python
# tests/property/test_compressor.py
from hypothesis import given, strategies as st

# Feature: news-article-aggregator, Property 6: Compression round-trip
@given(st.text(min_size=1, max_size=10000))
def test_compression_round_trip(content):
    compressor = ContentCompressor()
    compressed = compressor.compress(content)
    decompressed = compressor.decompress(compressed)
    assert decompressed == content
```

## 🎯 Key Implementation Guidelines

### Backend

1. **Use Async Handlers**
```python
@router.get("/articles")
async def get_articles():
    # Use async/await for I/O operations
    articles = await article_store.query_articles()
    return APIResponse(success=True, data=articles)
```

2. **Use Error Handling Decorators**
```python
from src.core.error_handler import retry_with_backoff, handle_errors

@retry_with_backoff(max_retries=3)
@handle_errors
async def fetch_article(url: str):
    # Your code here
    pass
```

3. **Use Structured Logging**
```python
from src.core.logger import logger, LogContext

logger.info("Processing article", extra_fields={"article_id": "123"})

with LogContext(logger, request_id="abc", user_id="user1"):
    logger.info("This log will include request_id and user_id")
```

4. **Use Custom Exceptions**
```python
from src.core.exceptions import ArticleNotFoundError

if not article:
    raise ArticleNotFoundError(f"Article {article_id} not found")
```

### Frontend

1. **Use API Service**
```javascript
import api from './services/api';

const fetchArticles = async () => {
  try {
    const response = await api.getArticles({ page: 1, page_size: 20 });
    setArticles(response.data);
  } catch (error) {
    console.error('Failed to fetch articles:', error.message);
  }
};
```

2. **Use Error Boundary**
```javascript
import ErrorBoundary from './components/ErrorBoundary';

<ErrorBoundary>
  <YourComponent />
</ErrorBoundary>
```

3. **Use Loading States**
```javascript
import LoadingSpinner from './components/LoadingSpinner';

{loading && <LoadingSpinner message="Loading articles..." />}
```

## 📚 Useful Commands

### Docker
```bash
# Rebuild services
docker-compose up -d --build

# Stop services
docker-compose down

# View logs
docker-compose logs -f [service_name]

# Execute commands in container
docker-compose exec backend bash
docker-compose exec postgres psql -U newsagg -d news_aggregator
```

### Database
```bash
# Create migration
cd backend
alembic revision --autogenerate -m "Create articles table"

# Run migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Frontend
```bash
cd frontend

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint
```

## 🐛 Troubleshooting

### Backend won't start
- Check if PostgreSQL is running: `docker-compose ps postgres`
- Check logs: `docker-compose logs backend`
- Verify environment variables in `.env`

### Frontend can't connect to API
- Check if backend is running: `curl http://localhost:8000/api/v1/health`
- Check Vite proxy configuration in `vite.config.js`
- Check CORS settings in `backend/src/main.py`

### Database connection issues
- Verify DATABASE_URL in `.env`
- Check PostgreSQL logs: `docker-compose logs postgres`
- Test connection: `docker-compose exec postgres psql -U newsagg -d news_aggregator`

## 📖 Additional Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **React Docs**: https://react.dev/
- **Tailwind CSS**: https://tailwindcss.com/docs
- **Hypothesis (PBT)**: https://hypothesis.readthedocs.io/
- **Docker Compose**: https://docs.docker.com/compose/

## 🎓 Learning Path

1. Start with Task 2 (Content Compressor) - simplest component
2. Write property tests as you implement features
3. Use the provided error handling and logging utilities
4. Follow the design document for implementation details
5. Test each component before moving to the next

## 💡 Tips

- ✅ Commit frequently with descriptive messages
- ✅ Write tests before or alongside implementation
- ✅ Use the provided utilities (logger, error handlers, response classes)
- ✅ Follow the task list order for smooth progress
- ✅ Check the design document for technical details
- ✅ Use Docker Compose for consistent environment

---

**Ready to build? Start with Task 2 in `tasks.md`! 🚀**
