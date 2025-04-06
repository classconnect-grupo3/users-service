# app/services/user_service.py
from sqlalchemy.orm import Session
from app.errors.user_errors import UserAlreadyExistsError
from app.repositories.user_repository import get_user, db_create_user, db_get_users
from app.schemas.user import UserBase
from app.models.user_model import User
from app.common.result import Success, Failure, Result


def create_new_user(db: Session, user: UserBase) -> Result[User]:
    existing_user = get_user(db, user.name, user.surname)
    if existing_user:
        return Failure(UserAlreadyExistsError())
    new_user = db_create_user(db=db, user=user)
    return Success(new_user)


# Service to get all users
def get_all_users(db: Session):
    return db_get_users(db=db)
