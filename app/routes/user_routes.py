from fastapi import APIRouter, HTTPException, status
from app.schemas.user_schema import UserCreate, UserUpdate, UserInDB
from app.models import user as user_model

router = APIRouter()

# CREATE a user
@router.post("/", response_model=UserInDB, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    """
    Create a new user in the database.
    """
    new_user = await user_model.create_user(user.model_dump())
    if isinstance(new_user, str):
        if new_user == "Duplicate Username":
            raise HTTPException(status_code=409, detail="Username duplicate. Try another one.")
        elif new_user == "Incomplete Data":
            raise HTTPException(status_code=422, detail="User data not completed")
    return new_user

# GET a single user by ID
@router.get("/{user_id}", response_model=UserInDB)
async def get_user(user_id: str):
    """
    Get a user by their ID.
    """
    user = await user_model.retrieve_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# UPDATE a user
@router.patch("/{user_id}", response_model=UserInDB)
async def update_user(user_id: str, user_data: UserUpdate):
    """
    Update an existing user's information by ID.
    """
    updated_user = await user_model.update_user(user_id, user_data.model_dump(exclude_unset=True))
    if isinstance(updated_user, str):
        if updated_user == "Duplicate Username":
            raise HTTPException(status_code=409, detail="Username duplicate. Try another one.")
        elif updated_user == "No Exist User":
            raise HTTPException(status_code=404, detail="User not found")
    return updated_user

# DELETE a user
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str):
    """
    Delete a user by ID.
    """
    deleted = await user_model.delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return None

# LIST all users
@router.get("/", response_model=list[UserInDB])
async def list_users():
    """
    List all users in the database.
    """
    return await user_model.list_users()

# Follow another user
@router.patch("/{user_id}/follow/{target_id}")
async def follow(user_id: str, target_id: str):
    """
    Get user follow another user by perspective ID
    """
    success = await user_model.follow_user(user_id, target_id)
    if isinstance(success, str):
        if success == "Self Follow":
            raise HTTPException(status_code=409, detail="Cannot do self-following.")
        elif success == "No Exist User":
            raise HTTPException(status_code=400, detail="Invalid follower or target ID. Please check your input.")
        elif success == "Not Modified":
            raise HTTPException(status_code=409, detail=f"User {user_id} already followed user with ID {target_id}")
    return {"message": f"User {user_id} followed user with ID {target_id}"}

# Unfollow a user
@router.patch("/{user_id}/unfollow/{target_id}")
async def unfollow(user_id: str, target_id: str):
    """
    Get user unfollow another user by perspective ID
    """
    success = await user_model.unfollow_user(user_id, target_id)
    if isinstance(success, str):
        if success == "No Exist User":
            raise HTTPException(status_code=400, detail="Invalid follower or target ID. Please check your input.")
        elif success == "Not Modified":
            raise HTTPException(status_code=409, detail=f"User {user_id} wasn't following user with ID {target_id}")
    return {"message": f"User {user_id} unfollowed user with ID {target_id}"}

# Get followers
@router.get("/{user_id}/followers")
async def followers(user_id: str):
    """
    Get the list of follower by ID  
    """
    result = await user_model.get_followers(user_id)
    return {"followers": result}

# Get following
@router.get("/{user_id}/following")
async def following(user_id: str):
    """
    Get the list of following by ID  
    """
    result = await user_model.get_following(user_id)
    return {"following": result}

# Get neary by following
@router.get("/{username}/nearby-friends")
async def get_nearby_friends(username: str, distance: int = 1000):
    """
    Return nearby friends (people they follow) by Username within X meters. Default X is 1000
    """
    nearby = await user_model.find_nearby_friends(username, max_distance_m=distance)
    return {"nearby_friends": nearby}