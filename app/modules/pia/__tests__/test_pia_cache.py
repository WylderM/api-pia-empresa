import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_cache_hit():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Login
        await ac.post("/auth/register", json={
            "email": "cache@test.com",
            "name": "Cache Test",
            "password": "123456"
        })
        token_res = await ac.post("/auth/token", data={
            "username": "cache@test.com",
            "password": "123456"
        })
        token = token_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Primeira consulta
        res1 = await ac.get("/pia/?ano=2021", headers=headers)
        assert res1.status_code == 200

        # Segunda consulta (espera cache)
        res2 = await ac.get("/pia/?ano=2021", headers=headers)
        assert res2.status_code == 200
        assert res1.text == res2.text  # conteúdo deve ser idêntico
