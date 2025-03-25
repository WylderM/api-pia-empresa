import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_user_crud_flow():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Register
        user_data = {
            "email": "user@example.com",
            "name": "User Test",
            "password": "user123"
        }
        response = await ac.post("/auth/register", json=user_data)
        assert response.status_code == 200

        # Login
        response = await ac.post("/auth/token", data={
            "username": user_data["email"],
            "password": user_data["password"]
        })
        assert response.status_code == 200
        token = response.json()["access_token"]

        headers = {"Authorization": f"Bearer {token}"}

        # Get all users
        response = await ac.get("/users/", headers=headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

        user_id = response.json()[0]["id"]

        # Get by ID
        response = await ac.get(f"/users/{user_id}", headers=headers)
        assert response.status_code == 200
        assert response.json()["email"] == user_data["email"]

        # Update user
        update_data = {
            "email": "updated@example.com",
            "name": "Updated User",
            "password": "newpass123"
        }
        response = await ac.put(f"/users/{user_id}", json=update_data, headers=headers)
        assert response.status_code == 200
        assert response.json()["email"] == "updated@example.com"

        # Delete user
        response = await ac.delete(f"/users/{user_id}", headers=headers)
        assert response.status_code == 204
