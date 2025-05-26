from app.schemas.error_response import ErrorResponse
from app.schemas.user import UserProfileResponse


block_user_response = {
    201: {
        "description": "User blocked successfully",
        "model": UserProfileResponse,
    },
    400: {"description": "User is already blocked", "model": ErrorResponse},
    404: {
        "description": "User not found",
        "model": ErrorResponse,
    },
    500: {
        "description": "Internal server error",
        "model": ErrorResponse,
    },
}
