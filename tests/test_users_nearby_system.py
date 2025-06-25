import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport
from app.main import app

# Test Following and Unfollowing User
@pytest.mark.asyncio
async def test_nearby_user():
    
    list_test_user = [
        {
            "username": "test_user_1",
            "name": "Test User 1",
            "dob": "1999-12-31",
            "address": "123 Testing Lane",
            "description": "Just a test user",
            "location": {
                "type": "Point",
                "coordinates": [103.8198,1.3521]
            }
        },
        {
            "username": "test_user_2",
            "name": "Test User 2",
            "dob": "1999-12-31",
            "address": "123 Testing Lane",
            "description": "Just a test user",
            "location": {
                "type": "Point",
                "coordinates": [103.8200,1.3530]
            }
        },
        {
            "username": "test_user_3",
            "name": "Test User 3",
            "dob": "1999-12-31",
            "address": "123 Testing Lane",
            "description": "Just a test user",
            "location": {
                "type": "Point",
                "coordinates": [103.8200,1.2903]
            }
        },
        {
            "username": "test_user_4",
            "name": "Test User 4",
            "dob": "1999-12-31",
            "address": "123 Testing Lane",
            "description": "Just a test user",
            "location": {
                "type": "Point",
                "coordinates": [103.8500,1.2800]
            }
        },
        {
            "username": "test_user_5",
            "name": "Test User 5",
            "dob": "1999-12-31",
            "address": "123 Testing Lane",
            "description": "Just a test user",
            "location": {
                "type": "Point",
                "coordinates": [103.8000,1.4500]
            }
        }
    ]

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        
        # Create Necessary Dummy User for Test
        user_id = {}
        for test_user in list_test_user:
            response = await ac.post("/users/", json=test_user)
            user = response.json()
            user_id[test_user['name']] = {"id": user["id"], "username": user["username"]}

        # Create following scenarion for testing nearby API
        response = await ac.patch(f"/users/{user_id['Test User 1']['id']}/follow/{user_id['Test User 2']['id']}")
        assert response.status_code == 200

        response = await ac.patch(f"/users/{user_id['Test User 1']['id']}/follow/{user_id['Test User 3']['id']}")
        assert response.status_code == 200

        response = await ac.patch(f"/users/{user_id['Test User 1']['id']}/follow/{user_id['Test User 4']['id']}")
        assert response.status_code == 200

        response = await ac.patch(f"/users/{user_id['Test User 1']['id']}/follow/{user_id['Test User 5']['id']}")
        assert response.status_code == 200

        # Test Nearby Friends API
        response = await ac.get(f"/users/{user_id['Test User 1']['username']}/nearby-friends?distance=10000")
        assert response.status_code == 200

        nearby_friends = response.json()["nearby_friends"]
        friend_names = [friend["username"] for friend in nearby_friends]

        # Within Range
        assert "test_user_2" in friend_names
        assert "test_user_3" in friend_names
        assert "test_user_4" in friend_names

        # Out of Range (too far)
        assert "test_user_5" not in friend_names
        
        # Check Error Handling
        response = await ac.get(f"/users/123123123/nearby-friends?distance=10000")
        assert response.status_code == 200

        # Delete Dummy User as the test case already completede
        for one_user_id in user_id.keys():
            response = await ac.delete(f"/users/{user_id[one_user_id]}")