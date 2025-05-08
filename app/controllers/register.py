from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.common.result import Failure
from app.database.db import get_db
from app.errors.register_errors import CouldNotCreateFirebaseUser, UserAlreadyExists
from app.schemas.error_response import ErrorResponse
from app.schemas.user import UserBase, UserRegisterResponse
from app.services.register import create_new_user
from app.common.http_responses.register import register_responses

router = APIRouter()


# Create a new user (POST request)
@router.post("", status_code=201, responses=register_responses)
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
