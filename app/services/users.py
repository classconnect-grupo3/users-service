from app.errors.forgot_password import EmailSendingError
from fastapi import Request
from typing import List
from firebase_admin import (
    auth,
    exceptions as firebase_exceptions,
)

from dotenv import load_dotenv
import os
from email.message import EmailMessage
import aiosmtplib

load_dotenv()

from pydantic import EmailStr
from app.errors.generic_errors import (
    UserIsAlreadyAnAdmin,
    UserIsAlreadyBlocked,
    UserIsNotBlocked,
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
    get_users_by_ids_db,
    unlock_user_db,
    block_user_db,
    make_admin_db,
)
from app.schemas.user import UserProfileData, UserProfileUpdate
from app.errors.user_errors import (
    UserNotFoundError,
    UpdateProfileError,
    EmailAlreadyInUseError,
    NoUsersFoundError,
)


EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")


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


def update_user_profile_service(
    db: Session, update_data: UserProfileUpdate, token: str
) -> Success | Failure:
    result = get_uid_from_token(token)
    if isinstance(result, Failure):
        return result

    uid = result.value
    user = get_user_by_uid_db(db, uid)
    if not user:
        return Failure(UserNotFoundError())

    if update_data.email:
        existing_user = get_user_by_email_db(db, update_data.email)
        if existing_user and existing_user.uid != uid:
            return Failure(EmailAlreadyInUseError())

    try:
        auth.update_user(uid, email=update_data.email)
    except firebase_exceptions.FirebaseError as e:
        return Failure(InvalidTokenError(message=f"Firebase error: {str(e)}"))

    return update_user_profile_db(db, user, update_data)


def search_users_service(db: Session, query: str) -> Success | Failure:
    return search_users_db(db, query)


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


def get_user_info_by_email(db: Session, email: str):
    user = get_user_by_email_db(db, email)
    return {
        "uid": user.uid,
        "name": user.name,
        "surname": user.surname,
        "is_admin": user.is_admin,
        "latitude": user.latitude,
        "longitude": user.longitude,
    }


def get_user_location(db: Session, email: str):
    user = get_user_by_email_db(db, email)
    return {"latitude": user.latitude, "longitude": user.longitude}


def is_user_active_by_email(email: EmailStr, db: Session) -> Success | Failure:
    user = get_user_by_email_db(db, email)
    if not user:
        return Failure(UserNotFoundError())

    return Success(user.is_active)


def make_admin_by(email: EmailStr, db: Session) -> Success | Failure:
    user = get_user_by_email_db(db, email)
    if not user:
        return Failure(UserNotFoundError())

    if user.is_admin:
        return Failure(UserIsAlreadyAnAdmin())

    return make_admin_db(db, user)


def block_user_by(email: EmailStr, db: Session) -> Success | Failure:
    user = get_user_by_email_db(db, email)
    if not user:
        return Failure(UserNotFoundError())

    if user.is_blocked:
        return Failure(UserIsAlreadyBlocked())

    return block_user_db(db, user)


def unlock_user_by(email: EmailStr, db: Session) -> Success | Failure:
    user = get_user_by_email_db(db, email)
    if not user:
        return Failure(UserNotFoundError())

    if not user.is_blocked:
        return Failure(UserIsNotBlocked())

    return unlock_user_db(db, user)


async def send_password_reset_link(email: str) -> Success | Failure:
    try:
        reset_link = auth.generate_password_reset_link(email)
    except auth.UserNotFoundError:
        return Failure(UserNotFoundError(email=email))
    except Exception as e:
        return Failure(EmailSendingError(reason=f"Failed to generate link: {e}"))

    return await send_reset_email(email, reset_link)


async def send_reset_email(to_email: str, reset_link: str) -> Success | Failure:
    try:
        message = EmailMessage()
        message["From"] = EMAIL_ADDRESS
        message["To"] = to_email
        message["Subject"] = "Reset your password"
        message.set_content(f"Click here to reset your password: {reset_link}")

        await aiosmtplib.send(
            message,
            hostname="smtp.gmail.com",
            port=587,
            start_tls=True,
            username=EMAIL_ADDRESS,
            password=EMAIL_APP_PASSWORD,
        )
        return Success("Password reset email sent successfully.")
    except Exception as e:
        return Failure(EmailSendingError(reason=f"SMTP error: {e}"))
