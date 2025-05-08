from app.common.constants import OK
from app.errors.firebase_errors import (
    ArgumentsMissingError,
    CertificateFetchError,
    ExpiredIdTokenError,
    InvalidIdTokenError,
    RevokedIdTokenError,
    UserDisabledError,
)
from sqlalchemy.orm import Session
from firebase_admin import auth, exceptions

from app.common.result import Success, Failure
from app.repositories.register_verify_phone import activate_user_phone
from app.errors.user_errors import FirebaseTokenInvalidError


def verify_user_phone_service(id_token: str, db: Session):
    try:
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token.get("uid")
        phone_number = decoded_token.get("phone_number")

        if not uid or not phone_number:
            return Failure(
                ArgumentsMissingError("UID or phone number missing in token.")
            )

        result = db_activate_user_phone(db, uid, phone_number)
        if isinstance(result, Failure):
            return Failure(result)
        return Success(OK)

    except auth.InvalidIdTokenError:
        return Failure(InvalidIdTokenError())
    except auth.ExpiredIdTokenError:
        return Failure(ExpiredIdTokenError())
    except auth.RevokedIdTokenError:
        return Failure(RevokedIdTokenError())
    except auth.CertificateFetchError:
        return Failure(CertificateFetchError())
    except auth.UserDisabledError:
        return Failure(UserDisabledError())
    except Exception as e:
        return Failure(ValueError(f"An unexpected error occurred: {str(e)}"))
