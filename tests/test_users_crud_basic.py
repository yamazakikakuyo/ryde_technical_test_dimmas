import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport
from app.main import app

# Test All Basic Operation with Best Scenario (no Error)
@pytest.mark.asyncio
async def test_create_get_update_delete_user():
    
    # Sample user payload for test
    test_user = {
        "name": "Test User",
        "dob": "1999-12-31",
        "address": "123 Testing Lane",
        "description": "Just a test user",
        "location": {
            "type": "Point",
            "coordinates": [106.8456, -6.2088]
        }
    }

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Create user
        response = await ac.post("/users/", json=test_user)
        assert response.status_code == 201
        user = response.json()
        user_id = user["id"]
        assert user["name"] == test_user["name"]

        # Get user
        response = await ac.get(f"/users/{user_id}")
        assert response.status_code == 200
        assert response.json()["id"] == user_id

        # Update user
        updated_data = {"address": "456 Updated Ave"}
        response = await ac.patch(f"/users/{user_id}", json=updated_data)
        assert response.status_code == 200
        assert response.json()["address"] == updated_data["address"]

        # Delete user
        response = await ac.delete(f"/users/{user_id}")
        assert response.status_code == 204

        # Try to get deleted user
        response = await ac.get(f"/users/{user_id}")
        assert response.status_code == 404

# Test Error Handling for Create User request with missing fields
@pytest.mark.asyncio
async def test_create_user_missing_fields():
    incomplete_user = {"name": "No DOB or Address"}
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/users/", json=incomplete_user)
        assert response.status_code == 422

# Test Error Handling for Searching User with Fake ID
@pytest.mark.asyncio
async def test_get_nonexistent_user():
    fake_id = "123"
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get(f"/users/{fake_id}")
        assert response.status_code in [404, 400]

# Test Error Handling for creating user with wrong date format
@pytest.mark.asyncio
async def test_create_user_with_invalid_date():
    bad_date_user = {
        "name": "Invalid DOB",
        "dob": "31-12-1999",  # Wrong format
        "address": "1 Fake St",
        "description": "Bad date format",
        "location": {
            "type": "Point",
            "coordinates": [106.8456, -6.2088]
        }
    }
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/users/", json=bad_date_user)
        assert response.status_code == 422