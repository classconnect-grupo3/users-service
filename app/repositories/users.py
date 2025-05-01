from typing import Optional
from pytest import Session
from app.schemas.user import UserProfileData
from app.models.user_model import User


def store_location_db(db: Session, uid: str, latitude: float, longitude: float):
    user = db.query(User).filter(User.uid == uid).first()
    user.latitude = latitude
    user.longitude = longitude
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

def search_users_db(db: Session, query: str) -> list[User]:
    terms = query.split()
    
    if not terms:
        return []

    if len(terms) == 1:
        term = f"%{terms[0]}%"
        filters = or_(
            User.name.ilike(term),
            User.surname.ilike(term)
        )
    else:
        name = f"%{terms[0]}%"
        surname = f"%{terms[1]}%"
        filters = or_(
            and_(User.name.ilike(name), User.surname.ilike(surname)),
            and_(User.name.ilike(surname), User.surname.ilike(name)),
            User.name.ilike(name),
            User.surname.ilike(surname)
        )

    return db.query(User).filter(filters).distinct().all()