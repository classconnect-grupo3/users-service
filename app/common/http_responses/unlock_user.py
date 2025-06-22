from app.schemas.error_response import ErrorResponse
from app.schemas.user import UserProfileResponse

unlock_user_response = {
    201: {
        "description": "User unlocked successfully",
        "model": UserProfileResponse,
    },
    400: {"description": "User is not blocked", "model": ErrorResponse},
    404: {
        "description": "User not found",
        "model": ErrorResponse,
    },
    500: {
        "description": "Internal server error",
        "model": ErrorResponse,
    },
}
