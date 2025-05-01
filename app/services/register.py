# app/service/register.py
import os

import anyio
from firebase_admin import auth
from firebase_admin import exceptions as firebase_exceptions
from sqlalchemy.orm import Session

from app.common.result import Failure, Result, Success
from app.errors.register_errors import CouldNotCreateFirebaseUser, UserAlreadyExists
from app.models.user_model import User
from app.repositories.register import db_create_user
from app.schemas.user import UserBase
from app.repositories.users import get_user_by_email_db

# Use env variable to determine if we're in test mode
ENVIRONMENT = os.getenv("ENVIRONMENT", "development").lower()


def create_firebase_user(email: str, password: str):
    try:
        user = auth.create_user(
            email=email,
            password=password,
        )
        return Success(user)
    except ValueError as e:
        # Handle invalid password or other validation errors
        return Failure(CouldNotCreateFirebaseUser(message=f"Invalid input: {str(e)}"))
    except firebase_exceptions.FirebaseError as e:
        # Handle Firebase-specific errors
        return Failure(CouldNotCreateFirebaseUser(message=f"Firebase error: {str(e)}"))


async def create_new_user(db: Session, user: UserBase) -> Result[User]:
    existing_user = get_user_by_email_db(db, user.email)
    if existing_user:
        return Failure(UserAlreadyExists())

    firebase_result = await anyio.to_thread.run_sync(
        create_firebase_user, user.email, user.password
    )

    if isinstance(firebase_result, Failure):
        return firebase_result

    firebase_user = firebase_result.value

    new_user = db_create_user(db=db, user=user, uid=firebase_user.uid)

    return Success(new_user)
