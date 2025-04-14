import os
from firebase_admin import auth
from fastapi import Request

import requests
from sqlalchemy.orm import Session

from app.common.db_functions import get_user
from app.common.result import Failure, Success
from app.errors.authentication_errors import (
    CertificateFetchError,
    ExpiredTokenError,
    InvalidCredentialsError,
    InvalidTokenError,
    RevokedTokenError,
    UIDNotFoundError,
)
from app.repositories.login_with_email import store_location_db
from app.schemas.auth_request import AuthRequest


# Get values from environment variables with defaults
FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY")
FIREBASE_AUTH_URL = os.getenv(
    "FIREBASE_AUTH_URL",
    "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword",
)


def verify_email_and_password(auth_request: AuthRequest):
    url = FIREBASE_AUTH_URL
    params = {"key": FIREBASE_API_KEY}
    payload = {
        "email": auth_request.email,
        "password": auth_request.password,
        "returnSecureToken": True,
    }
    response = requests.post(url, params=params, json=payload, timeout=10)
    if response.status_code == 200:
        id_token = response.json().get("idToken")

        return Success(id_token)

    error_message = response.json().get("error", {}).get("message", "Unknown error")

    return Failure(
        InvalidCredentialsError(message=f"Authentication failed: {error_message}")
    )


def get_user_location(db: Session, email: str):
    user = get_user(db, email)
    return user.location


def store_location(db: Session, location: str, token: str):
    # Validate the token and get the UID
    result = get_uid_from_token(token)
    if isinstance(result, Failure):
        return result

    uid = result.value

    # Store the location in the database
    store_location_db(db, uid, location)

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
