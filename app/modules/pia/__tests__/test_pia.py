import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_fetch_pia_data():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Primeiro, cadastrar e logar usuário
        await ac.post("/auth/register", json={
            "email": "pia@test.com",
            "name": "PIA Test",
            "password": "123456"
        })
        res = await ac.post("/auth/token", data={
            "username": "pia@test.com",
            "password": "123456"
        })
        token = res.json()["access_token"]

        headers = {"Authorization": f"Bearer {token}"}

        # Buscar dados (vazio no início)
        res = await ac.get("/pia/", headers=headers)
        assert res.status_code == 200
        assert isinstance(res.json(), list)
