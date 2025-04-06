from sqlalchemy.orm import Session

from app.repositories.repository import db_create_user, db_get_users
from app.schemas.user import UserBase, User


# Service to create a user
def create_new_user(db: Session, user: UserBase) -> User:
    return db_create_user(db=db, user=user)


# Service to get all users
def get_all_users(db: Session):
    return db_get_users(db=db)