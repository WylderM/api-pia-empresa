import pytest
from httpx import AsyncClient
from app.main import app
from app.core.db import override_get_db, TestingSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession

app.dependency_overrides[override_get_db] = override_get_db

@pytest.mark.asyncio
async def test_register_and_login():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Register
        response = await ac.post("/auth/register", json={
            "email": "test@example.com",
            "name": "Test User",
            "password": "123456"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "test@example.com"

        # Login
        response = await ac.post("/auth/token", data={
            "username": "test@example.com",
            "password": "123456"
        })
        assert response.status_code == 200
        token = response.json()["access_token"]
        assert token

        # Get Current User
        response = await ac.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200
        assert response.json()["email"] == "test@example.com"
