from sqlalchemy.orm import Session
from app.repositories.user_repository import db_create_user, db_get_users, get_user
from app.schemas.user import UserBase, User


# Service to create a user
def create_new_user(db: Session, user: UserBase) -> User:
    existing_user = get_user(db, user.name, user.surname)
    if existing_user:
        return None
    
    return db_create_user(db=db, user=user)


# Service to get all users
def get_all_users(db: Session):
    return db_get_users(db=db)