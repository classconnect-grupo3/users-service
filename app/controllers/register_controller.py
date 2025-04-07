from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from app.database.db import get_db
from app.errors.user_errors import UserAlreadyExistsError
from app.schemas.error_response import ErrorResponse
from app.schemas.user import AllUsersResponse, UserBase, UserResponse
from app.common.result import Failure
from app.services.user_service import create_new_user, get_all_users

router = APIRouter()


# Create a new user (POST request)
@router.post(
    "/",
    status_code=201,
    responses={
        201: {"description": "User created successfully", "model": UserResponse},
        400: {"description": "Bad request error", "model": ErrorResponse},
        409: {
            "description": "Conflict error - user already exists",
            "model": ErrorResponse,
        },
    },
)
def create_user(user: UserBase, db: Session = Depends(get_db)):

    result = create_new_user(db, user)
    if isinstance(result, Failure):
        error = result.error
        if isinstance(error, UserAlreadyExistsError):
            raise HTTPException(
                status_code=409, detail=str(error), headers={"X-Error": "Conflict"}
            )

    return {"data": result.value}


# Get all users (GET request)
# @router.get(
#     "/",
#     response_model=AllUsersResponse,
#     responses={
#         200: {"description": "A list of users", "model": AllUsersResponse},
#     },
# )
# def get_users(db: Session = Depends(get_db)):

#     users = get_all_users(db=db)

#     return {"data": users}
