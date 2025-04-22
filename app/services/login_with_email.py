import os


import requests
from sqlalchemy.orm import Session

from app.common.result import Failure, Success
from app.errors.authentication_errors import InvalidCredentialsError
from app.schemas.auth_request import AuthRequest
from app.repositories.users import get_user_by_email_db

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
    user = get_user_by_email_db(db, email)
    return {"latitude": user.latitude, "longitude": user.longitude}
