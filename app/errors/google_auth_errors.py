class GoogleAuthError(Exception):
    """Base class for all Google authentication-related errors."""
    def __init__(self, message: str, http_status_code: int):
        super().__init__(message)
        self.message = message
        self.http_status_code = http_status_code


class ValueError(GoogleAuthError):
    """Raised when id_token is not a string or is empty."""
    def __init__(self, message: str = "The id_token must be a non-empty string."):
        super().__init__(message, http_status_code=400)


class InvalidIdTokenError(GoogleAuthError):
    """Raised when id_token is not a valid Firebase ID token."""
    def __init__(self, message: str = "The id_token is not a valid Firebase ID token."):
        super().__init__(message, http_status_code=401)


class ExpiredIdTokenError(GoogleAuthError):
    """Raised when the specified ID token has expired."""
    def __init__(self, message: str = "The ID token has expired."):
        super().__init__(message, http_status_code=401)


class RevokedIdTokenError(GoogleAuthError):
    """Raised when the ID token has been revoked."""
    def __init__(self, message: str = "The ID token has been revoked."):
        super().__init__(message, http_status_code=401)

class ArgumentsMissingError(GoogleAuthError):
    """Raised when the id_token is missing uid or email."""
    def __init__(self, message: str):
        super().__init__(message, http_status_code=401)

class UserDisabledError(GoogleAuthError):
    """Raised when the user record is disabled."""
    def __init__(self, message: str = "The user associated with the ID token is disabled."):
        super().__init__(message, http_status_code=403)

        
class CertificateFetchError(GoogleAuthError):
    """Raised when an error occurs while fetching public key certificates."""
    def __init__(self, message: str = "Failed to fetch public certificates for token verification."):
        super().__init__(message, http_status_code=500)




        