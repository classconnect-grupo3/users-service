from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from app.config.database.db import get_db
from app.schemas.error_response import ErrorResponse
from app.schemas.user import AllUsersResponse, UserBase, UserResponse
from app.services.service import create_new_user, get_all_users

router = APIRouter()


# Create a new user (POST request)
@router.post(
    "/",
    responses={
        201: {"description": "User created successfully", "model": UserResponse},
        400: {"description": "Bad request error", "model": ErrorResponse},
    },
)
def create_user(user: UserBase, db: Session = Depends(get_db)):

    user = create_new_user(db=db, user=user)

    if not user:
        return HTTPException(
            status_code=409,
            detail="User with this name and surname already exists",
        )

    return {"data": user}


# Get all users (GET request)
@router.get(
    "/",
    response_model=AllUsersResponse,
    responses={
        200: {"description": "A list of users", "model": AllUsersResponse},
    },
)
def get_users(db: Session = Depends(get_db)):

    users = get_all_users(db=db)

    return {"data": users}