from app.schemas.google_auth_result import GoogleAuthResult
from app.schemas.error_response import ErrorResponse

login_responses = {
    200: {
        "description": "User authenticated successfully",
        "model": GoogleAuthResult,
    },
    401: {
        "description": "Unauthorized: Invalid or expired token",
        "content": {
            "application/json": {
                "examples": {
                    "invalid_token": {
                        "summary": "Invalid token",
                        "value": {
                            "detail": "The token provided is invalid.",
                        },
                    },
                    "expired_token": {
                        "summary": "Expired token",
                        "value": {
                            "detail": "The token has expired. Please log in again.",
                        },
                    },
                    "revoked_token": {
                        "summary": "Revoked token",
                        "value": {
                            "detail": "The token has been revoked.",
                        },
                    },
                    "invalid_credentials": {
                        "summary": "Invalid credentials",
                        "value": {
                            "detail": "Invalid email or password.",
                        },
                    },
                }
            }
        },
        "model": ErrorResponse,
    },
    403: {
        "description": "Forbidden: User account disabled",
        "content": {
            "application/json": {
                "examples": {
                    "user_disabled": {
                        "summary": "User disabled",
                        "value": {
                            "detail": "The user account is disabled.",
                        },
                    },
                }
            }
        },
        "model": ErrorResponse,
    },
    500: {
        "description": "Internal Server Error: Certificate fetch error or unexpected error",
        "content": {
            "application/json": {
                "examples": {
                    "certificate_fetch_error": {
                        "summary": "Certificate fetch error",
                        "value": {
                            "detail": "Failed to fetch public certificates for token verification.",
                        },
                    },
                    "unexpected_error": {
                        "summary": "Unexpected error",
                        "value": {
                            "detail": "An unexpected error occurred.",
                        },
                    },
                }
            }
        },
        "model": ErrorResponse,
    },
    
}