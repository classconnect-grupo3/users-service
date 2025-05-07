from app.common.result import Success, Failure
from app.repositories.login_with_google import create_user_from_google_db
from app.schemas.auth_google_request import GoogleAuthRequest
from firebase_admin import auth as firebase_auth
from app.errors.google_auth_errors import InvalidGoogleTokenError
from app.common.constants import OK


def authenticate_with_google(request: GoogleAuthRequest):
    try:
        # Verify the token with Firebase
        decoded_token = firebase_auth.verify_id_token(request.id_token)
        uid = decoded_token.get("uid")
        name = decoded_token.get("name", "")
        email = decoded_token.get("email")

        if not email or not uid:
            return Failure(InvalidGoogleTokenError("UID or email not found in token."))

        name_parts = name.strip().split(" ")
        first_name = name_parts[0]
        last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else None

        result = create_user_from_google_db(
            uid=uid,
            name=first_name,
            surname=last_name,
            email=email,
        )

        if isinstance(result, Failure):
            return Failure(result.error)

        return Success(OK)

    except Exception as e:
        return Failure(InvalidGoogleTokenError(e))
