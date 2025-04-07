# app/services/user_service.py
from sqlalchemy.orm import Session
from app.common.db_functions import get_user
from app.errors.register_errors import UserAlreadyExists
from app.repositories.register import db_create_user
from app.schemas.user import UserBase
from app.models.user_model import User
from app.common.result import Success, Failure, Result


def create_new_user(db: Session, user: UserBase) -> Result[User]:
    existing_user = get_user(db, user.email)
    if existing_user:
        return Failure(UserAlreadyExists())
    new_user = db_create_user(db=db, user=user)
    return Success(new_user)



