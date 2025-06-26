from app.schemas.error_response import ErrorResponse
from app.schemas.user import UserIsAdminResponse

is_admin_response = {
    200: {
        "description": "User admin status retrieved successfully",
        "model": UserIsAdminResponse,
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
