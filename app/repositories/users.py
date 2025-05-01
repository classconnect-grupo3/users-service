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
    terms = [term.strip() for term in query.split() if term.strip()]
    print("TÉRMINOS DE BÚSQUEDA:", terms)

    if not terms:
        return []

    filters = []
    for term in terms:
        like_term = f"%{term}%"
        filters.append(User.name.ilike(like_term))
        filters.append(User.surname.isnot(None)) 
        filters.append(User.surname.ilike(like_term))

    final_filter = or_(*filters)
    query_sql = db.query(User).filter(final_filter).distinct()

    print("SQL:", str(query_sql))
    results = query_sql.all()
    print("RESULTADOS:", [u.email for u in results])
    return results