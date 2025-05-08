from app.common.result import Failure, Success
from app.errors.database_errors import DatabaseError
from app.repositories.users import get_user_by_email_db
from sqlalchemy.orm import Session
from app.common.constants import OK

from app.models.user_model import User


def create_user_from_google_db(
    db: Session, uid: str, name: str, surname: str, email: str
):
    try:
        user = get_user_by_email_db(db, email)
        if user:
            return Success(True)  # Ya estaba registrado

        # Si no existe, lo creamos
        new_user = User(
            uid=uid,
            name=name,
            surname=surname,
            email=email,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return Success(False)  # No estaba registrado antes
    except Exception as e:
        return Failure(DatabaseError(str(e)))
