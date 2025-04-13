from pytest import Session
from app.models.user_model import User as DBUser


def get_user(db: Session, email: str):
    return db.query(DBUser).filter_by(email=email).first()
