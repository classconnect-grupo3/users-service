class AuthenticationError(Exception):
    def __init__(self, message: str, http_status_code: int):
        super().__init__(message)
        self.http_status_code = http_status_code


class IncorrectPassword(AuthenticationError):
    def __init__(self, message: str = "Incorrect password."):
        super().__init__(message, http_status_code=401)


class UserNotFound(AuthenticationError):
    def __init__(self, message: str = "User not found."):
        super().__init__(message, http_status_code=404)
