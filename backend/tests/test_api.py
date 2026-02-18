"""Integration tests for API routes"""
import pytest
from httpx import AsyncClient, ASGITransport
from src.main import app


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


class TestAPIRoutes:
    """Integration tests for FastAPI endpoints"""

    @pytest.mark.asyncio
    async def test_root_endpoint(self, client):
        response = await client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert data["version"] == "1.0.0"

    @pytest.mark.asyncio
    async def test_health_endpoint(self, client):
        response = await client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["status"] == "healthy"

    @pytest.mark.asyncio
    async def test_get_articles_empty(self, client):
        response = await client.get("/api/v1/articles")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert isinstance(data["data"], list)

    @pytest.mark.asyncio
    async def test_get_articles_with_pagination(self, client):
        response = await client.get("/api/v1/articles?page=1&page_size=10")
        assert response.status_code == 200
        data = response.json()
        assert data["page"] == 1
        assert data["page_size"] == 10

    @pytest.mark.asyncio
    async def test_get_nonexistent_article(self, client):
        response = await client.get("/api/v1/articles/nonexistent-id-12345")
        assert response.status_code in [404, 500]

    @pytest.mark.asyncio
    async def test_get_clusters_empty(self, client):
        response = await client.get("/api/v1/clusters")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data

    @pytest.mark.asyncio
    async def test_get_stats(self, client):
        response = await client.get("/api/v1/stats")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "total_articles" in data["data"]

    @pytest.mark.asyncio
    async def test_invalid_date_format(self, client):
        response = await client.get("/api/v1/articles?date_from=invalid-date")
        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_pagination_validation(self, client):
        response = await client.get("/api/v1/articles?page=-1")
        assert response.status_code == 422  # Pydantic validation error

    @pytest.mark.asyncio
    async def test_page_size_validation(self, client):
        response = await client.get("/api/v1/articles?page_size=500")
        assert response.status_code == 422  # Exceeds max
