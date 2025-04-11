class AuthenticationError(Exception):
    def __init__(self, message: str, http_status_code: int):
        super().__init__(message)
        self.message = message
        self.http_status_code = http_status_code


class InvalidCredentialsError(AuthenticationError):
    def __init__(self, message: str = "Invalid email or password."):
        super().__init__(message, http_status_code=401)
