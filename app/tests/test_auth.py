import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

transport = ASGITransport(app=app)

@pytest.mark.asyncio
async def test_register_and_login():
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/auth/register", json={
            "email": "test@example.com",
            "name": "Test User",
            "password": "123456"
        })
        assert response.status_code == 200

        response = await ac.post("/auth/token", data={
            "username": "test@example.com",
            "password": "123456"
        })
        assert response.status_code == 200
        assert "access_token" in response.json()