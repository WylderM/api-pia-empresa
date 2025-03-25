import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

transport = ASGITransport(app=app)

@pytest.mark.asyncio
async def test_status_and_health():
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        r = await ac.get("/status")
        assert r.status_code == 200
        assert r.json()["status"] == "ok"

        r = await ac.get("/health")
        assert r.status_code == 200
        assert "database" in r.json()