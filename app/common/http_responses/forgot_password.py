from app.schemas.error_response import ErrorResponse

forgot_password_responses = {
    202: {
        "description": "Password reset email sent successfully",
    },
    400: {
        "description": "Bad request error",
        "model": ErrorResponse,
    },
    404: {
        "description": "User not found",
        "model": ErrorResponse,
    },
    500: {
        "description": "Internal server error",
        "model": ErrorResponse,
    },
    502: {
        "description": "Failed to send reset email",
        "model": ErrorResponse,
    },
}
