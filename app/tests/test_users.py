import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

transport = ASGITransport(app=app)

@pytest.mark.asyncio
async def test_user_crud_flow():
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        await ac.post("/auth/register", json={
            "email": "user@test.com",
            "name": "User",
            "password": "123456"
        })
        token_response = await ac.post("/auth/token", data={
            "username": "user@test.com",
            "password": "123456"
        })
        token = token_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        response = await ac.get("/users/", headers=headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)
