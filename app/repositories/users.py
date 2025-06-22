from typing import Optional, List
from app.errors.generic_errors import EmptySearchTermsError, UidOrEmailNotProvided
from app.errors.user_errors import NoUsersFoundError
from pytest import Session
from app.schemas.user import UserProfileData, UserProfileUpdate
from app.models.user_model import User
from sqlalchemy.sql import or_
from app.common.constants import NEW_USER, OK
from app.common.result import Failure, Success
from app.errors.database_errors import DatabaseError
from sqlalchemy.orm import Session

from app.models.user_model import User


def store_location_db(db: Session, uid: str, latitude: float, longitude: float):
    user = db.query(User).filter(User.uid == uid).first()
    user.latitude = latitude
    user.longitude = longitude
    db.commit()


def get_user_by_uid_db(db: Session, uid: str):
    return db.query(User).filter(User.uid == uid).first()


def update_user_profile_db(
    db: Session, user: User, profile_data: UserProfileUpdate
) -> Success | Failure:
    try:
        for field, value in profile_data.dict(exclude_unset=True).items():
            setattr(user, field, value)
        db.commit()
        db.refresh(user)
        return Success(user)
    except Exception as e:
        return Failure(DatabaseError(str(e)))


def get_user_by_email_db(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def search_users_db(db: Session, query: str) -> Success | Failure:
    try:
        terms = [term.strip() for term in query.split() if term.strip()]

        if not terms:
            return Failure(EmptySearchTermsError())

        filters = []
        for term in terms:
            like_term = f"%{term}%"
            filters.append(User.name.ilike(like_term))
            filters.append(User.surname.ilike(like_term))

        final_filter = or_(*filters)

        users = db.query(User).filter(final_filter).distinct().all()

        if not users:
            return Failure(NoUsersFoundError())

        return Success(users)
    except Exception as e:
        return Failure(DatabaseError(str(e)))


def get_users_by_ids_db(db: Session, user_ids: List[str]) -> list[User]:
    return db.query(User).filter(User.uid.in_(user_ids)).all()


# Create a user in the database
def store_user_in_db(
    uid: str,
    name,
    email,
    db: Session,
    surname=None,
    phone=None,
    latitude=None,
    longitude=None,
    is_active=False,
    is_blocked=False,
):
    try:
        db_user = User(
            uid=uid,
            name=name,
            surname=surname,
            email=email,
            phone=phone,
            latitude=latitude,
            longitude=longitude,
            is_active=is_active,
            is_blocked=is_blocked,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return Success(db_user)
    except Exception as e:
        return Failure(DatabaseError(str(e)))


# Admin metrics functions
def get_user_stats_db(db: Session) -> Success | Failure:
    try:
        total_users = db.query(User).count()
        active_users = db.query(User).filter(User.is_active == True).count()
        inactive_users = db.query(User).filter(User.is_active == False).count()
        blocked_users = db.query(User).filter(User.is_blocked == True).count()
        admin_users = db.query(User).filter(User.is_admin == True).count()
        users_with_phone = db.query(User).filter(User.phone.isnot(None)).count()
        users_without_phone = db.query(User).filter(User.phone.is_(None)).count()
        users_with_location = db.query(User).filter(
            User.latitude.isnot(None), 
            User.longitude.isnot(None)
        ).count()
        users_without_location = db.query(User).filter(
            or_(User.latitude.is_(None), User.longitude.is_(None))
        ).count()
        
        return Success({
            "total_users": total_users,
            "active_users": active_users,
            "inactive_users": inactive_users,
            "blocked_users": blocked_users,
            "admin_users": admin_users,
            "users_with_phone": users_with_phone,
            "users_without_phone": users_without_phone,
            "users_with_location": users_with_location,
            "users_without_location": users_without_location
        })
    except Exception as e:
        return Failure(DatabaseError(str(e)))




def block_user_db(db: Session, user: User):
    try:
        user.is_blocked = True
        db.commit()
        db.refresh(user)
        return Success(user)
    except Exception as e:
        return Failure(DatabaseError(str(e)))


def make_admin_db(db: Session, user: User):
    try:
        user.is_admin = True
        db.commit()
        db.refresh(user)
        return Success(user)
    except Exception as e:
        return Failure(DatabaseError(str(e)))

def unlock_user_db(db: Session, user: User):
    try:
        user.is_blocked = False
        db.commit()
        db.refresh(user)
        return Success(user)