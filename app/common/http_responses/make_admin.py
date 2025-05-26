from app.schemas.error_response import ErrorResponse
from app.schemas.user import UserProfileResponse


make_admin_response = {
    201: {
        "description": "User updated to Admin successfully",
        "model": UserProfileResponse,
    },
    400: {"description": "User is already an admin", "model": ErrorResponse},
    404: {
        "description": "User not found",
        "model": ErrorResponse,
    },
    500: {
        "description": "Internal server error",
        "model": ErrorResponse,
    },
}
