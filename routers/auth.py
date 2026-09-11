from fastapi import APIRouter, HTTPException, status

from models.user_request import UserRequest
from models.login_request import LoginRequest
from services.user_service import UserService
from utils.token import create_access_token


router = APIRouter()

user_service = UserService()


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: UserRequest):
    new_user = user_service.register_user(
        user.username,
        user.password
    )

    if new_user is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists"
        )

    return {
        "message": "User registered successfully"
    }


@router.post("/login")
def login(user: LoginRequest):
    authenticated_user = user_service.authenticate_user(
        user.username,
        user.password
    )

    if authenticated_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    access_token = create_access_token(
        authenticated_user.id
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }