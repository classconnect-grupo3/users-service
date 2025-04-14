from pytest import Session

from app.models.user_model import User


def store_location_db(db: Session, uid: str, location: str):
    user = db.query(User).filter(User.uid == uid).first()
    user.location = location
    db.commit()
