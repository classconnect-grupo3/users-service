from app.schemas.auth_result import AuthResult
from app.schemas.error_response import ErrorResponse

login_responses = {
    200: {
        "description": "User authenticated successfully",
        "content": {
            "application/json": {
                "examples": {
                    "with_location": {
                        "summary": "Example with location",
                        "value": {
                            "id_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                            "user_location": "Argentina",
                        },
                    },
                    "without_location": {
                        "summary": "Example without location",
                        "value": {
                            "id_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                            "user_location": None,
                        },
                    },
                }
            }
        },
        "model": AuthResult,
    },
    404: {
        "description": "User not found",
        "model": ErrorResponse,
    },
    401: {
        "description": "Unauthorized: Incorrect password",
        "model": ErrorResponse,
    },
}
