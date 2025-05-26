class ForgotPasswordError(Exception):
    def __init__(self, message: str, http_status_code: int):
        super().__init__(message)
        self.message = message
        self.http_status_code = http_status_code


class UserNotFoundError(ForgotPasswordError):
    http_status_code = 404
    def __init__(self, email: str):
        self.message = f"User with email {email} not found."

class EmailSendingError(ForgotPasswordError):
    http_status_code = 502
    def __init__(self, reason: str = "Failed to send email."):
        self.message = reason