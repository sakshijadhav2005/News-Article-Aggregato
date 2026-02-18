FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download ML models for faster startup
RUN python -c "from transformers import T5ForConditionalGeneration, T5Tokenizer; \
    T5Tokenizer.from_pretrained('t5-small'); \
    T5ForConditionalGeneration.from_pretrained('t5-small')" || true

RUN python -c "from sentence_transformers import SentenceTransformer; \
    SentenceTransformer('all-MiniLM-L6-v2')" || true

# Copy application code
COPY . .

# Create logs directory
RUN mkdir -p logs

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD python -c "import requests; r = requests.get('http://localhost:8000/'); assert r.status_code == 200" || exit 1

# Run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
