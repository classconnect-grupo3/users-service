class GenericError(Exception):
    def __init__(self, message: str, http_status_code: int):
        super().__init__(message)
        self.message = message
        self.http_status_code = http_status_code


class UidOrEmailNotProvided(GenericError):
    def __init__(self, message: str = "Either uid or email must be provided"):
        super().__init__(message, http_status_code=400)


class UserIsAlreadyAnAdmin(GenericError):
    def __init__(self, message: str = "User is already an admin"):
        super().__init__(message, http_status_code=400)


class CouldNotUpdateUser(GenericError):
    def __init__(self, message: str = "Could not update user"):
        super().__init__(message, http_status_code=500)


class UserNotProvided(GenericError):
    def __init__(self, message: str = "User not provided"):
        super().__init__(message, http_status_code=400)


class UserIsAlreadyBlocked(GenericError):
    def __init__(self, message: str = "User is already blocked"):
        super().__init__(message, http_status_code=400)


class UserIsNotBlocked(GenericError):
    def __init__(self, message: str = "User is not blocked"):
        super().__init__(message, http_status_code=400)


class EmptySearchTermsError(GenericError):
    def __init__(
        self,
        message: str = "No search terms provided. Please enter at least one term to search.",
    ):
        super().__init__(message, http_status_code=400)
