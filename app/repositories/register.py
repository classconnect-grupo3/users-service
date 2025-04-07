from sqlalchemy.orm import Session
from app.models.user_model import User as DBUser
from app.schemas.user import UserBase
from app.common.security import hash_password 


# Create a user in the database
def db_create_user(db: Session, user: UserBase):
    hashed_password = hash_password(user.password)
    db_user = DBUser(
        name=user.name,
        surname=user.surname,
        email=user.email,
        password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
