import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport
from app.main import app

# Test Following and Unfollowing User
@pytest.mark.asyncio
async def test_following_and_unfollowing_user():
    
    list_test_user = [
        {
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
            "name": "Test User 3",
            "dob": "1999-12-31",
            "address": "123 Testing Lane",
            "description": "Just a test user",
            "location": {
                "type": "Point",
                "coordinates": [103.8520,1.2903]
            }
        },
        {
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
            print(user)
            user_id[test_user['name']] = user["id"]

        # Check Follow API Usage
        response = await ac.patch(f"/users/{user_id['Test User 1']}/follow/{user_id['Test User 2']}")
        assert response.status_code == 200

        response = await ac.patch(f"/users/{user_id['Test User 1']}/follow/{user_id['Test User 3']}")
        assert response.status_code == 200

        response = await ac.patch(f"/users/{user_id['Test User 1']}/follow/{user_id['Test User 4']}")
        assert response.status_code == 200

        response = await ac.patch(f"/users/{user_id['Test User 2']}/follow/{user_id['Test User 1']}")
        assert response.status_code == 200

        response = await ac.patch(f"/users/{user_id['Test User 4']}/follow/{user_id['Test User 5']}")
        assert response.status_code == 200

        response = await ac.patch(f"/users/{user_id['Test User 5']}/follow/{user_id['Test User 4']}")
        assert response.status_code == 200

        # Check Get Following and Follower API Usage alongside crosscheck result of Follow API 
        response = await ac.get(f"/users/{user_id['Test User 1']}/following")
        assert response.status_code == 200
        list_following = response.json()["following"]
        assert user_id['Test User 2'] in list_following
        assert user_id['Test User 3'] in list_following

        response = await ac.get(f"/users/{user_id['Test User 2']}/following")
        assert response.status_code == 200
        list_following = response.json()["following"]
        assert user_id['Test User 1'] in list_following

        response = await ac.get(f"/users/{user_id['Test User 4']}/following")
        assert response.status_code == 200
        list_following = response.json()["following"]
        assert user_id['Test User 5'] in list_following

        response = await ac.get(f"/users/{user_id['Test User 5']}/following")
        assert response.status_code == 200
        list_following = response.json()["following"]
        assert user_id['Test User 4'] in list_following

        response = await ac.get(f"/users/{user_id['Test User 1']}/followers")
        assert response.status_code == 200
        list_followers = response.json()["followers"]
        assert user_id['Test User 2'] in list_followers

        response = await ac.get(f"/users/{user_id['Test User 2']}/followers")
        assert response.status_code == 200
        list_followers = response.json()["followers"]
        assert user_id['Test User 1'] in list_followers

        response = await ac.get(f"/users/{user_id['Test User 3']}/followers")
        assert response.status_code == 200
        list_followers = response.json()["followers"]
        assert user_id['Test User 1'] in list_followers

        response = await ac.get(f"/users/{user_id['Test User 5']}/followers")
        assert response.status_code == 200
        list_followers = response.json()["followers"]
        assert user_id['Test User 4'] in list_followers

        response = await ac.get(f"/users/{user_id['Test User 4']}/followers")
        assert response.status_code == 200
        list_followers = response.json()["followers"]
        assert user_id['Test User 5'] in list_followers

        # Check Unfollow API Usage
        response = await ac.patch(f"/users/{user_id['Test User 1']}/unfollow/{user_id['Test User 2']}")
        assert response.status_code == 200

        # Crosscheck result of unfollow API 
        response = await ac.get(f"/users/{user_id['Test User 1']}/following")
        assert response.status_code == 200
        list_following = response.json()["following"]
        assert user_id['Test User 2'] not in list_following

        response = await ac.get(f"/users/{user_id['Test User 2']}/followers")
        assert response.status_code == 200
        list_followers = response.json()["followers"]
        assert user_id['Test User 1'] not in list_followers

        # Check Error Handling of following same user
        response = await ac.patch(f"/users/{user_id['Test User 1']}/follow/{user_id['Test User 1']}")
        assert response.status_code == 400

        # Check Error Handling of following where follower non-existance user
        response = await ac.patch(f"/users/123123123/follow/{user_id['Test User 1']}")
        assert response.status_code == 400

        # Check Error Handling of following where target non-existance user
        response = await ac.patch(f"/users/{user_id['Test User 1']}/follow/123123123")
        assert response.status_code == 400

        # Delete Dummy User as the test case already completede
        for one_user_id in user_id.keys():
            response = await ac.delete(f"/users/{user_id[one_user_id]}")