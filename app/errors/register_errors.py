class RegisterUserError(Exception):
    def __init__(self, message: str, http_status_code: int):
        super().__init__(message)
        self.message = message
        self.http_status_code = http_status_code


class UserAlreadyExists(RegisterUserError):
    def __init__(self, message: str = "User with this email already exists"):
        super().__init__(message, http_status_code=409)


class CouldNotCreateFirebaseUser(RegisterUserError):
    def __init__(self, message: str):
        super().__init__(message, http_status_code=502)
