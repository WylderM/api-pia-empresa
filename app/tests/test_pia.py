import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.core.db import engine, Base

transport = ASGITransport(app=app)

@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@pytest.mark.asyncio
async def test_pia_filter():
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        await ac.post("/auth/register", json={
            "email": "pia@test.com",
            "name": "Pia User",
            "password": "123456"
        })
        token_response = await ac.post("/auth/token", data={
            "username": "pia@test.com",
            "password": "123456"
        })
        token = token_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        response = await ac.get("/pia/?ano=2021", headers=headers)
        assert response.status_code == 200
