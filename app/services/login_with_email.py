# app/services/user_service.py
from sqlalchemy.orm import Session
from app.common.db_functions import get_user
from app.common.security import verify_password
from app.errors.authentication_errors import IncorrectPassword, UserNotFound
from app.common.result import Result, Success, Failure
from app.schemas.auth_request import AuthRequest


def authenticate_user_with_email(data: AuthRequest, db: Session) -> Result[int]:
    user = get_user(db, data.email)
    if not user:
        return Failure(UserNotFound())
    if not verify_password(data.password, user.password):
        return Failure(IncorrectPassword())
    return Success(1)