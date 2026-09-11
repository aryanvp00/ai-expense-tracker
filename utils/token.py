from jose import jwt


SECRET_KEY = "change-this-later"
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