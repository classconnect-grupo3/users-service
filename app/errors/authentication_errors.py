class AuthenticationError(Exception):
    def __init__(self, message: str, http_status_code: int):
        super().__init__(message)
        self.message = message
        self.http_status_code = http_status_code


class UIDNotFoundError(AuthenticationError):
    def __init__(self, message: str = "UID not found in token."):
        super().__init__(message, http_status_code=400)


class InvalidCredentialsError(AuthenticationError):
    def __init__(self, message: str = "Invalid email or password."):
        super().__init__(message, http_status_code=401)


class ExpiredTokenError(AuthenticationError):
    def __init__(self, message: str = "Token has expired."):
        super().__init__(message, http_status_code=401)


class RevokedTokenError(AuthenticationError):
    def __init__(self, message: str = "Token has been revoked."):
        super().__init__(message, http_status_code=401)


class InvalidTokenError(AuthenticationError):
    def __init__(self, message: str = "Invalid token."):
        super().__init__(message, http_status_code=401)


class CertificateFetchError(AuthenticationError):
    def __init__(
        self,
        message: str = "Failed to fetch public certificates for token verification.",
    ):
        super().__init__(message, http_status_code=500)
