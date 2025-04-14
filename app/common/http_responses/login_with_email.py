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
                            "id_token": "String",
                            "user_location": "String",
                        },
                    },
                    "without_location": {
                        "summary": "Example without location",
                        "value": {
                            "id_token": "String",
                            "user_location": "This field is returned with NULL",
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
