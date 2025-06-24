import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

# Load environment variables from .env file
load_dotenv()

# Calling connection string to MongoDB from .env
MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise Exception("MONGO_URI not found in environment variables")

# For create new session of database everytime called. 
# This is due to Async Motor Client bug in Windows which make the variable cannot be reused
def get_database_session():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client["ryde_users_db"]
    db["users"].create_index([("location", "2dsphere")])
    return db

# Initialization for Index Creation upon app startup
# Currently the index only 2dspehere for location search 
async def init_db_indexes():
    db = get_database_session()
    await db["users"].create_index([("location", "2dsphere")])