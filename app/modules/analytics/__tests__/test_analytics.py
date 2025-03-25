import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_top_setores():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Registro e login
        await ac.post("/auth/register", json={
            "email": "analytics@test.com",
            "name": "Analytics",
            "password": "123456"
        })
        res = await ac.post("/auth/token", data={
            "username": "analytics@test.com",
            "password": "123456"
        })
        token = res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Testar top setores
        res = await ac.get("/analytics/top-setores?ano=2021&variavel=Valor da transformação", headers=headers)
        assert res.status_code == 200
        assert isinstance(res.json(), list)
