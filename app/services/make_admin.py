from app.common.result import Failure, Success
from app.errors.generic_errors import UserIsAlreadyAnAdmin
from app.errors.user_errors import UserNotFoundError
from app.repositories.users import get_user_by_email_db, update_user_db, update_user_profile_db
from app.schemas.user import UserProfileUpdate
from sqlalchemy.orm import Session
from pydantic import EmailStr


def make_admin_by(email: EmailStr, db: Session) -> Success | Failure:
    user = get_user_by_email_db(db, email)
    if not user:
        return Failure(UserNotFoundError())

    if user.is_admin:
        return Failure(UserIsAlreadyAnAdmin())

    update_data = UserProfileUpdate(is_admin=True)

    result = update_user_profile_db(db, user, update_data)
    if isinstance(result, Failure):
        return Failure(result)

    return Success(result)
