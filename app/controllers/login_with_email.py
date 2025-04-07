from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from app.database.db import get_db
from app.errors.authentication_errors import IncorrectPassword, UserNotFound
from app.schemas.error_response import ErrorResponse
from app.common.result import Failure
from app.schemas.auth_request import AuthRequest
from app.services.login_with_email import authenticate_user_with_email

router = APIRouter()


# Authenticate user with email and password
@router.post(
    "",
    status_code=200,
    responses={
        200: {"description": "User authenticated successfully"},
        404: {"description": "User not found", "model": ErrorResponse},
        401: {
            "description": "Unauthorized: Incorrect password",
            "model": ErrorResponse,
        },
    },
)
def login_user(data: AuthRequest, db: Session = Depends(get_db)):
    result = authenticate_user_with_email(data, db)

    if isinstance(result, Failure):
        error = result.error
        if isinstance(error, IncorrectPassword):
            raise HTTPException(
                status_code=error.http_status_code, detail=error.message
            )
        if isinstance(error, UserNotFound):
            raise HTTPException(
                status_code=error.http_status_code, detail=error.message
            )
