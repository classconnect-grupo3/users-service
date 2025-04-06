from sqlalchemy.orm import Session
from app.models.user_model import User as DBUser
from app.schemas.user import UserBase


# Create a user in the database
def db_create_user(db: Session, user: UserBase):
    db_user = DBUser(name=user.name, surname=user.surname)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# Get all users from the database
def db_get_users(db: Session):
    return db.query(DBUser).all()