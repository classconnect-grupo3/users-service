from app.schemas.result_auth import AuthResult
from app.schemas.error_response import ErrorResponse
from app.schemas.user import UserRegisterResponse

register_responses = {
    201: {
        "description": "User created successfully",
        "model": UserRegisterResponse,
    },
    400: {"description": "Bad request error", "model": ErrorResponse},
    409: {
        "description": "User already exists",
        "model": ErrorResponse,
    },
    502: {
        "description": "Could not create Firebase user",
        "model": ErrorResponse,
    },
}
