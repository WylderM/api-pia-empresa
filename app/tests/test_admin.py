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
async def test_status_and_health():
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        r = await ac.get("/status")
        assert r.status_code == 200
        assert r.json()["status"] == "ok"

        r = await ac.get("/health")
        assert r.status_code == 200
        assert "database" in r.json()
