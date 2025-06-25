from datetime import datetime, timezone, date
from uuid import uuid4
from app.db.mongo import get_database_session

from app.core.logging_config import logger

# Reference to the MongoDB "users" collection
user_collection_name = "users"

# Helper to format MongoDB result to match our schema
def user_helper(user) -> dict:
    return {
        "id": str(user.get("_id")),
        "username": user.get("username"),
        "name": user.get("name"),
        "dob": str(user.get("dob")) if user.get("dob") else None,
        "address": user.get("address"),
        "description": user.get("description"),
        "createdAt": user.get("createdAt"),
        "followers": user.get("followers", []),
        "following": user.get("following", []),
        "location": user.get("location")
    }

# CRUD OPERATIONS (to be called from the route layer)

async def create_user(data: dict) -> dict:
    """Insert a new user into the database."""
    data["_id"] = str(uuid4())
    data["createdAt"] = datetime.now(timezone.utc).isoformat()

    # Convert dob from datetime.date to datetime.datetime
    if isinstance(data.get("dob"), date):
        data["dob"] = datetime.combine(data["dob"], datetime.min.time())

    username_check = await get_database_session().get_collection(user_collection_name).find_one({"username": data["username"]})
    if username_check:
        logger.error(f"Failed Created User. Username ({data['username']}) already used by other user")
        return "Duplicate Username"

    return_data = user_helper(data)
    for datum in return_data.keys():
        if return_data[datum] == None:
            logger.error("Mandatory User Information Not Complete. Failed to create user.")
            return "Incomplete Data"
    
    await get_database_session().get_collection(user_collection_name).insert_one(data)
    
    return return_data

async def retrieve_user(user_id: str) -> dict:
    """Retrieve a single user by ID."""
    user = await get_database_session().get_collection(user_collection_name).find_one({"_id": user_id})
    if user:
        logger.info(f"Get User Information with ID {user_id}")
        return user_helper(user)
    else:
        logger.error(f"Failed Get User Information. The user with ID {user_id} is Non-Existance User")
        return None

async def update_user(user_id: str, data: dict) -> dict:
    """Update user info."""
    
    if "dob" in data and isinstance(data["dob"], date):
        data["dob"] = datetime.combine(data["dob"], datetime.min.time())

    await get_database_session().get_collection(user_collection_name).update_one({"_id": user_id}, {"$set": data})
    user = await get_database_session().get_collection(user_collection_name).find_one({"_id": user_id})
    if user:
        logger.info(f"Update User Information with ID {user_id}")
        return user_helper(user)
    else:
        logger.error(f"Failed Update User Information with ID  {user_id}")
        return None

async def delete_user(user_id: str) -> bool:
    """Delete a user by ID."""
    result = await get_database_session().get_collection(user_collection_name).delete_one({"_id": user_id})
    return_result = result.deleted_count == 1
    if return_result:
        logger.info(f"Delete User Information with ID {user_id}")
    else:
        logger.error(f"Failed Delete User Information with ID {user_id}")
    return return_result

async def list_users() -> list:
    """Get all users in the database."""
    users = []
    async for user in get_database_session().get_collection(user_collection_name).find():
        users.append(user_helper(user))
    logger.info(f"Get List of User")
    return users

# Follow another user
async def follow_user(follower_id: str, target_id: str) -> bool:
    if follower_id == target_id:
        logger.error(f"Failed Follow. User with ID {follower_id} tried follow themself.")
        return False  # Prevent self-follow
    
    follower_user = await get_database_session().get_collection(user_collection_name).find_one({"_id": follower_id})
    target_user = await get_database_session().get_collection(user_collection_name).find_one({"_id": target_id})
    
    if follower_user is None or target_user is None:
        logger.error(f"Failed Follow. Either or both of Follower or Target User is non-existance.")
        return False # Prevent non-existance User

    # Update 'following' of follower
    await get_database_session().get_collection(user_collection_name).update_one(
        {"_id": follower_id},
        {"$addToSet": {"following": target_id}}
    )
    # Update 'followers' of target
    await get_database_session().get_collection(user_collection_name).update_one(
        {"_id": target_id},
        {"$addToSet": {"followers": follower_id}}
    )
    logger.info(f"User with ID {follower_id} followed user with ID {target_id}")
    return True

# Unfollow a user
async def unfollow_user(follower_id: str, target_id: str) -> bool:
    follower_user = await get_database_session().get_collection(user_collection_name).find_one({"_id": follower_id})
    target_user = await get_database_session().get_collection(user_collection_name).find_one({"_id": target_id})
    
    if follower_user is None or target_user is None:
        logger.error(f"Failed Follow. Either or both of Follower or Target User is non-existance.")
        return False # Prevent non-existance User

    await get_database_session().get_collection(user_collection_name).update_one(
        {"_id": follower_id},
        {"$pull": {"following": target_id}}
    )
    await get_database_session().get_collection(user_collection_name).update_one(
        {"_id": target_id},
        {"$pull": {"followers": follower_id}}
    )
    logger.info(f"User with ID {follower_id} unfollowed user with ID {target_id}")
    return True

# Get followers of a user
async def get_followers(user_id: str) -> list:
    user = await get_database_session().get_collection(user_collection_name).find_one({"_id": user_id})
    logger.info(f"Get Followers of User with ID {user_id}")
    return user.get("followers", []) if user else []

# Get following list of a user
async def get_following(user_id: str) -> list:
    user = await get_database_session().get_collection(user_collection_name).find_one({"_id": user_id})
    logger.info(f"Get Following of User with ID {user_id}")
    return user.get("following", []) if user else []

# Get nearby user following
async def find_nearby_friends(username: str, max_distance_m: int = 1000) -> list:
    user = await get_database_session().get_collection(user_collection_name).find_one({"username": username})
    if not user or "location" not in user:
        logger.error(f"Failed Get User Information. The user with username {username} is Non-Existance User")
        return None

    user_coords = user["location"]["coordinates"]
    friend_ids = user.get("following", [])  # or followers

    # Query users within radius who are in their "following" list
    cursor = get_database_session().get_collection(user_collection_name).find({
        "_id": {"$in": friend_ids},
        "location": {
            "$near": {
                "$geometry": {
                    "type": "Point",
                    "coordinates": user_coords
                },
                "$maxDistance": max_distance_m
            }
        }
    })

    nearby = []
    async for doc in cursor:
        nearby.append(user_helper(doc))
    logger.info(f"Get Nearby Following of User with ID {username}")
    return nearby
