import os
from dotenv import load_dotenv
load_dotenv()
from jose import jwt
SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"


def create_access_token(user_id):
    payload = {
        "sub": str(user_id)
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )