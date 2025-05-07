class GoogleAuthError(Exception):
    def __init__(self, message: str, http_status_code: int = 500):
        super().__init__(message)
        self.message = message
        self.http_status_code = http_status_code


class InvalidGoogleTokenError(GoogleAuthError):
    def __init__(self, message: str):
        super().__init__(message, http_status_code=400)

