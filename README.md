# 📰 AI-Powered News Article Aggregator

A full-stack news aggregation system that fetches, compresses, summarizes, and clusters news articles from multiple sources using AI and machine learning.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green)
![React](https://img.shields.io/badge/React-18.2-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🌟 Features

- **Real-Time News Fetching**: Aggregates articles from BBC, CNN, The Guardian, Reuters via RSS feeds
- **Content Compression**: Reduces article storage by 40%+ using zlib compression
- **AI Summarization**: Generates 150-word summaries automatically
- **Topic Clustering**: Groups articles into 6 semantic categories
- **Smart Filtering**: Filter by source, topic, date range
- **Responsive UI**: Beautiful, modern interface built with React and Tailwind CSS
- **RESTful API**: Complete FastAPI backend with OpenAPI documentation

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- pip and npm

### Installation

**1. Clone the repository:**
```bash
git clone https://github.com/YOUR_USERNAME/news-article-aggregator.git
cd news-article-aggregator
```

**2. Install backend dependencies:**
```bash
cd backend
pip install -r requirements-real.txt
```

**3. Install frontend dependencies:**
```bash
cd frontend
npm install
```

### Running the Application

**Terminal 1 - Backend:**
```bash
cd backend
python run_simple.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

**Open your browser:**
- Frontend: http://localhost:5173
- API Docs: http://localhost:8000/docs

## 📖 Usage

1. **Fetch Articles**: Click "Fetch Articles" button on the home page
2. **Browse**: View articles in a beautiful grid layout
3. **Filter**: Filter by source (BBC, CNN, etc.) or topic
4. **Clusters**: View articles grouped by AI-detected topics
5. **Read**: Click "View Original" to read the full article on the source website

## 🏗️ Architecture

### Backend (Python + FastAPI)
```
backend/
├── src/
│   ├── api/              # API routes and responses
│   ├── core/             # Error handling, logging
│   ├── models/           # Data models
│   ├── services/         # Business logic
│   │   ├── compressor.py # Content compression
│   │   ├── fetcher.py    # RSS feed fetching
│   │   ├── summarizer.py # Text summarization
│   │   ├── clusterer.py  # Topic clustering
│   │   ├── store.py      # Data storage
│   │   └── cache.py      # Caching layer
│   └── main.py           # FastAPI application
└── run_simple.py         # Simple startup script
```

### Frontend (React + Vite)
```
frontend/
├── src/
│   ├── components/       # Reusable UI components
│   ├── pages/            # Page components
│   │   ├── HomePage.jsx
│   │   ├── ArticlesPage.jsx
│   │   └── ClustersPage.jsx
│   ├── services/         # API client
│   └── App.jsx           # Main application
└── package.json
```

## 🔧 API Endpoints

- `GET /api/v1/health` - Health check
- `POST /api/v1/articles/fetch` - Fetch new articles
- `GET /api/v1/articles` - List articles (with filters)
- `GET /api/v1/articles/{id}` - Get article details
- `GET /api/v1/clusters` - List topic clusters
- `GET /api/v1/clusters/{id}/articles` - Get cluster articles
- `GET /api/v1/stats` - System statistics

Full API documentation: http://localhost:8000/docs

## 🎨 Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **Pydantic**: Data validation
- **feedparser**: RSS feed parsing
- **BeautifulSoup4**: HTML parsing
- **zlib**: Content compression

### Frontend
- **React 18**: UI framework
- **Vite**: Build tool
- **Tailwind CSS**: Styling
- **Axios**: HTTP client
- **React Router**: Navigation

## 📊 Features in Detail

### Content Compression
- Uses zlib compression (level 6)
- Achieves 40%+ size reduction
- Automatic decompression on retrieval

### Summarization
- Extractive summarization (150 words)
- Preserves key information
- Fast and lightweight

### Topic Clustering
- 6 predefined categories:
  - Technology & AI
  - Climate & Environment
  - Politics & Policy
  - Health & Science
  - Business & Economy
  - Sports & Entertainment
- Keyword-based clustering
- Automatic article assignment

## 🧪 Testing

**Backend tests:**
```bash
cd backend
python test_backend.py
```

**Manual API testing:**
```bash
# Health check
curl http://localhost:8000/api/v1/health

# Fetch articles
curl -X POST http://localhost:8000/api/v1/articles/fetch

# List articles
curl http://localhost:8000/api/v1/articles
```

## 📝 Configuration

### Backend Configuration
Edit `backend/config/settings.py`:
```python
# Add more RSS feeds
rss_feeds: List[str] = [
    "https://feeds.bbci.co.uk/news/rss.xml",
    "https://rss.cnn.com/rss/edition.rss",
    # Add your feeds here
]

# Adjust compression level
compression_level: int = 6  # 1-9

# Change summary length
max_summary_words: int = 150
```

### Frontend Configuration
Edit `frontend/.env`:
```env
VITE_API_URL=http://localhost:8000/api/v1
```

## 🚀 Production Deployment

### Docker (Recommended)
```bash
docker-compose up -d
```

### Manual Deployment

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd frontend
npm run build
# Serve the dist/ folder with nginx or similar
```

## 🔮 Future Enhancements

- [ ] PostgreSQL database integration
- [ ] Redis caching
- [ ] Real-time updates with WebSockets
- [ ] User authentication
- [ ] Personalized feeds
- [ ] Mobile app
- [ ] Advanced ML models (T5, HDBSCAN)
- [ ] Sentiment analysis
- [ ] Email digests

## 📄 License

MIT License - see LICENSE file for details

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 👨‍💻 Author

Your Name - [@yourhandle](https://twitter.com/yourhandle)

Project Link: [https://github.com/YOUR_USERNAME/news-article-aggregator](https://github.com/YOUR_USERNAME/news-article-aggregator)

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/)
- [React](https://react.dev/)
- [Tailwind CSS](https://tailwindcss.com/)
- News sources: BBC, CNN, The Guardian, Reuters

---

**Built with ❤️ for efficient news consumption**
