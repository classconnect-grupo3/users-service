from pytest import Session
from app.schemas.user import UserProfileData

from app.models.user_model import User


def store_location_db(db: Session, uid: str, location: str):
    user = db.query(User).filter(User.uid == uid).first()
    user.location = location
    db.commit()

def get_user_by_uid_db(db: Session, uid: str):
    return db.query(User).filter(User.uid == uid).first()


def update_user_profile_db(db: Session, uid: str, profile_data: UserProfileData):
    user = db.query(User).filter(User.uid == uid).first()
    if not user:
        return None

    for field, value in profile_data.dict(exclude_unset=True).items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user
    
def get_user_by_email_db(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()