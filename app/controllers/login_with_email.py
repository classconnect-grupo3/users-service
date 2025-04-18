from fastapi import APIRouter, Depends, HTTPException
from pytest import Session

from app.common.result import Failure
from app.database.db import get_db
from app.schemas.auth_request import AuthRequest
from app.schemas.auth_result import AuthResult
from app.services.login_with_email import get_user_location, verify_email_and_password
from app.common.http_responses.login_with_email import login_responses

router = APIRouter()


# Authenticate user with email and password
@router.post(
    "",
    status_code=200,
    responses=login_responses,
)
def login_user(auth_request: AuthRequest, db: Session = Depends(get_db)):

    result = verify_email_and_password(auth_request)
    if isinstance(result, Failure):
        error = result.error
        raise HTTPException(status_code=error.http_status_code, detail=error.message)

    user_location = get_user_location(db, auth_request.email)

    return AuthResult(
        id_token=result.value,
        user_location=user_location,
    )
