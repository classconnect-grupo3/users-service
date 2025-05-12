from fastapi import APIRouter, Depends, HTTPException
from app.schemas.token import Token, TokenRequest
from app.services.register_verify_phone import verify_user_phone_service
from sqlalchemy.orm import Session

from app.common.result import Failure
from app.database.db import get_db
from app.errors.register_errors import CouldNotCreateFirebaseUser, UserAlreadyExists
from app.schemas.error_response import ErrorResponse
from app.schemas.user import UserBase, UserRegisterResponse
from app.services.register import create_new_user
from app.common.http_responses.register import login_responses

router = APIRouter()


@router.post("/verify-phone", status_code=200)
def verify_phone(request: Token, db: Session = Depends(get_db)):
    result = verify_user_phone_service(request.id_token, db)
    if isinstance(result, Failure):
        error = result.error
        raise HTTPException(status_code=error.http_status_code, detail=error.message)

    return Token(
        id_token=request.id_token,
    )
