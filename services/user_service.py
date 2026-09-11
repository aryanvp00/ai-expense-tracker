from pymongo import MongoClient

from models.user import User
from utils.password import hash_password, verify_password


class UserService:
    # Handles user-related business logic

    def __init__(self):
        # Connect to MongoDB
        self.client = MongoClient("mongodb://localhost:27017/")

        # Select database
        self.db = self.client["expense_tracker"]

        # Select users collection
        self.collection = self.db["users"]

    def register_user(self, username, password):
        # Check whether username already exists
        existing_user = self.collection.find_one({
            "username": username
        })

        if existing_user is not None:
            return None

        # Hash the password
        password_hash = hash_password(password)

        # Create MongoDB document
        user_data = {
            "username": username,
            "password_hash": password_hash
        }

        # Save user
        result = self.collection.insert_one(user_data)

        # Add generated ID
        user_data["_id"] = result.inserted_id

        # Convert MongoDB document into User object
        return User.from_mongo(user_data)

    def authenticate_user(self, username, password):
        # Find user by username
        user_data = self.collection.find_one({
            "username": username
        })

        # User doesn't exist
        if user_data is None:
            return None

        # Verify entered password against stored hash
        if not verify_password(
            password,
            user_data["password_hash"]
        ):
            return None

        # Convert MongoDB document into User object
        return User.from_mongo(user_data)