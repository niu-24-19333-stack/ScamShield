# ===========================================
# ScamShield Backend Tests
# ===========================================

import pytest
from httpx import AsyncClient
from app.main import app


@pytest.fixture
def anyio_backend():
    return 'asyncio'


@pytest.mark.anyio
async def test_health_check():
    """Test the health check endpoint."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200


@pytest.mark.anyio
async def test_root():
    """Test the root endpoint."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/")
        assert response.status_code == 200


@pytest.mark.anyio
async def test_scan_requires_auth():
    """Test that scan endpoint requires authentication."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/scans/scan",
            json={"text": "test message"}
        )
        assert response.status_code == 401


@pytest.mark.anyio
async def test_register_user():
    """Test user registration."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "password": "SecurePass123!",
                "full_name": "Test User"
            }
        )
        # Should work or return conflict if user exists
        assert response.status_code in [200, 201, 400, 409]
