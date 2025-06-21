from app.schemas.error_response import ErrorResponse
from app.schemas.user import UserIsActiveResponse


is_active_response = {
    200: {
        "description": "User status retrieved successfully",
        "model": UserIsActiveResponse,
    },
    404: {
        "description": "User not found",
        "model": ErrorResponse,
    },
    500: {
        "description": "Internal server error",
        "model": ErrorResponse,
    },
}
