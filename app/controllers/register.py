from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.common.result import Failure
from app.database.db import get_db
from app.errors.register_errors import CouldNotCreateFirebaseUser, UserAlreadyExists
from app.schemas.error_response import ErrorResponse
from app.schemas.user import UserBase, UserResponse
from app.services.register import create_new_user

router = APIRouter()


# Create a new user (POST request)
@router.post(
    "",
    status_code=201,
    responses={
        201: {"description": "User created successfully", "model": UserResponse},
        400: {"description": "Bad request error", "model": ErrorResponse},
        409: {
            "description": "User already exists",
            "model": ErrorResponse,
        },
        502: {
            "description": "Could not create Firebase user",
            "model": ErrorResponse,
        },
    },
)
async def create_user(user: UserBase, db: Session = Depends(get_db)):

    result = await create_new_user(db, user)
    if isinstance(result, Failure):
        error = result.error
        if isinstance(error, UserAlreadyExists):
            raise HTTPException(
                status_code=error.http_status_code,
                detail=error.message,
                headers={"X-Error": "Conflict"},
            )
        if isinstance(error, CouldNotCreateFirebaseUser):
            raise HTTPException(
                status_code=error.http_status_code,
                detail=error.message,
                headers={"X-Error": "FirebaseError"},
            )
    return {"data": result.value}
