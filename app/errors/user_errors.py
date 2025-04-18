class UserError(Exception):
    def __init__(self, message: str, http_status_code: int = 400):
        super().__init__(message)
        self.message = message
        self.http_status_code = http_status_code


class UserNotFoundError(UserError):
    def __init__(self, message: str = "User not found"):
        super().__init__(message, http_status_code=404)


class UpdateProfileError(UserError):
    def __init__(self, message: str = "Failed to update user profile"):
        super().__init__(message, http_status_code=500)

