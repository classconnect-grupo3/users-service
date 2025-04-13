from sqlalchemy.orm import Session
from app.models.user_model import User as DBUser
from app.schemas.user import UserBase


# Create a user in the database
def db_create_user(db: Session, user: UserBase, uid: str):
    db_user = DBUser(
        uid=uid,
        name=user.name,
        surname=user.surname,
        email=user.email,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
