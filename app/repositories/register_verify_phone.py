from app.common.constants import OK
from sqlalchemy.orm import Session

from app.models.user_model import User
from app.common.result import Success, Failure
from app.errors.user_errors import UserNotFoundError


def db_activate_user_phone(db: Session, uid: str, phone: str):
    user = db.query(User).filter(User.uid == uid).first()
    if not user:
        return Failure(UserNotFoundError("User not found."))

    user.phone = phone
    user.is_active = True
    db.commit()
    return Success(OK)
