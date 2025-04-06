# app/errors/user_errors.py
class UserError(Exception):
    pass


class UserAlreadyExistsError(UserError):
    def __init__(self, message: str = "User with this name and surname already exists"):
        super().__init__(message)
