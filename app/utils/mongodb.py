from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, ConfigurationError
from dotenv import load_dotenv
import os

load_dotenv()
username = os.getenv("USER_NAME")
password = os.getenv("PASSWORD")
MONGODB_URI = os.getenv("DATABASE_URL")

FINAL_URI = f"mongodb+srv://{username}:{password}@{MONGODB_URI}"

if not FINAL_URI:
    raise ValueError("MONGODB_URI is not set in the environment variables.")

try:
    client = MongoClient(FINAL_URI, serverSelectionTimeoutMS=5000)  # 5-second timeout
    db = client.get_database("omega_backend")
    # Test the connection
    client.admin.command('ping')
except (ServerSelectionTimeoutError, ConfigurationError) as e:
    raise RuntimeError(f"Failed to connect to MongoDB: {e}")

def get_collection(collection_name: str):
    """Retrieve a MongoDB collection by name."""
    return db[collection_name]
