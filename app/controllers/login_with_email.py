from fastapi import APIRouter, HTTPException
from app.common.result import Failure
from app.schemas.auth_request import AuthRequest
from app.schemas.error_response import ErrorResponse
from app.services.login_with_email import verify_email_and_password


router = APIRouter()


# Authenticate user with email and password
@router.post(
    "",
    status_code=200,
    responses={
        200: {"description": "User authenticated successfully"},
        404: {"description": "User not found", "model": ErrorResponse},
        401: {
            "description": "Unauthorized: Incorrect password",
            "model": ErrorResponse,
        },
    },
)
def login_user(auth_request: AuthRequest):
    result = verify_email_and_password(auth_request)
    if isinstance(result, Failure):
        error = result.error
        raise HTTPException(status_code=error.http_status_code, detail=error.message)
    return {"idToken": result.value}
