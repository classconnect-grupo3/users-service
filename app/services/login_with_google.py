from app.common.result import Success, Failure
from firebase_admin import auth as firebase_auth
from app.common.constants import OK, OLD_USER
from app.repositories.users import get_user_by_email_db, store_user_in_db
from sqlalchemy.orm import Session
from app.errors.google_auth_errors import (
    ArgumentsMissingError,
    ValueError,
    InvalidIdTokenError,
    ExpiredIdTokenError,
    RevokedIdTokenError,
    CertificateFetchError,
    UserDisabledError,
)


def authenticate_with_google(
    id_token: str,
    db: Session,
):
    try:
        # Verify the token with Firebase
        decoded_token = firebase_auth.verify_id_token(id_token)
        uid = decoded_token.get("uid")
        name = decoded_token.get("name", "")
        email = decoded_token.get("email")

        if not email or not uid:
            return Failure(ArgumentsMissingError("UID or email not found in token."))

        name_parts = name.strip().split(" ")
        first_name = name_parts[0]
        last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else None

        user = get_user_by_email_db(db, email)
        if user:
            return Success(OLD_USER)  # Ya estaba registrado

        result = store_user_in_db(
            db=db,
            uid=uid,
            name=first_name,
            surname=last_name,
            email=email,
        )

        if isinstance(result, Failure):
            return Failure(result)

        return Success(result)

    except firebase_auth.InvalidIdTokenError:
        return Failure(InvalidIdTokenError())
    except firebase_auth.ExpiredIdTokenError:
        return Failure(ExpiredIdTokenError())
    except firebase_auth.RevokedIdTokenError:
        return Failure(RevokedIdTokenError())
    except firebase_auth.CertificateFetchError:
        return Failure(CertificateFetchError())
    except firebase_auth.UserDisabledError:
        return Failure(UserDisabledError())
    except Exception as e:
        return Failure(ValueError(f"An unexpected error occurred: {str(e)}"))
