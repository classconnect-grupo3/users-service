from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.schemas.auth_google_request import GoogleAuthRequest
from app.schemas.auth_result import AuthResult
from app.services.login_with_google import authenticate_with_google
from app.common.result import Failure
from app.common.http_responses.login_with_google import login_responses



router = APIRouter()

@router.post(
    "",
    status_code=200,
    responses=login_responses,
)
def login_with_google(request: GoogleAuthRequest, db: Session = Depends(get_db)):
    result = authenticate_with_google(request.id_token, db)

    if isinstance(result, Failure):
        error = result.error
        raise HTTPException(status_code=error.http_status_code, detail=error.message)

    return AuthResult(
        id_token=request.id_token,
        user_location=None,
    )


