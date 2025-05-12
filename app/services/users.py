from fastapi import Request
from typing import List
from firebase_admin import (
    auth,
    exceptions as firebase_exceptions,
)
from pytest import Session
from app.common.result import Failure, Success
from app.errors.authentication_errors import (
    CertificateFetchError,
    ExpiredTokenError,
    InvalidTokenError,
    RevokedTokenError,
    UIDNotFoundError,
)

from app.repositories.users import (
    store_location_db,
    get_user_by_uid_db,
    update_user_profile_db,
    get_user_by_email_db,
    search_users_db,
    get_users_by_ids_db
)
from app.schemas.user import UserProfileData
from app.errors.user_errors import (
    UserNotFoundError,
    UpdateProfileError,
    EmailAlreadyInUseError,
    NoUsersFoundError,
)


def store_location(db: Session, latitude: float, longitude: float, token: str):
    # Validate the token and get the UID
    result = get_uid_from_token(token)
    if isinstance(result, Failure):
        return result

    uid = result.value

    # Store the location in the database
    store_location_db(db, uid, latitude, longitude)

    return Success("Location stored successfully")


def get_uid_from_token(token: str) -> Success | Failure:
    try:
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token.get("uid")
        if not uid:
            return Failure(UIDNotFoundError())
        return Success(uid)
    except auth.ExpiredIdTokenError:
        return Failure(ExpiredTokenError())
    except auth.RevokedIdTokenError:
        return Failure(RevokedTokenError())
    except auth.InvalidIdTokenError:
        return Failure(InvalidTokenError())
    except auth.CertificateFetchError:
        return Failure(CertificateFetchError())


def extract_token_from_request(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return Failure(InvalidTokenError(message="Invalid or missing token"))

    token = auth_header.split(" ")[1]
    return Success(token)


def get_user_profile(db: Session, token: str) -> Success | Failure:
    result = get_uid_from_token(token)
    if isinstance(result, Failure):
        return result

    uid = result.value
    user = get_user_by_uid_db(db, uid)

    if not user:
        return Failure(UserNotFoundError())

    return Success(user)


def update_user_profile(
    db: Session, update_data: UserProfileData, token: str
) -> Success | Failure:
    result = get_uid_from_token(token)
    if isinstance(result, Failure):
        return result

    uid = result.value

    if update_data.email:
        existing_user = get_user_by_email_db(db, update_data.email)
        if existing_user and existing_user.uid != uid:
            return Failure(EmailAlreadyInUseError())

    try:
        auth.update_user(uid, email=update_data.email)
    except firebase_exceptions.FirebaseError as e:
        return Failure(InvalidTokenError(message=f"Firebase error: {str(e)}"))

    updated_user = update_user_profile_db(db, uid, update_data)
    if not updated_user:
        return Failure(UpdateProfileError())

    return Success(updated_user)

def search_users_service(db: Session, query: str) -> Success | Failure:
    users = search_users_db(db, query)
    
    if not users:
        return Failure(NoUsersFoundError())
    
    return Success(users)


def get_user_by_id_service(db: Session, user_id: str) -> Success | Failure:
    user = get_user_by_uid_db(db, user_id)

    if not user:
        return Failure(UserNotFoundError())

    return Success(user)    

def get_users_batch_service(db: Session, user_ids: List[str]) -> Success | Failure:
    users = get_users_by_ids_db(db, user_ids)

    if not users:
        return Failure(NoUsersFoundError())

    return Success(users)