from sqlalchemy import Column, String, Float

from app.database.db import Base


class User(Base):
    __tablename__ = "users"

    uid = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, default=None, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    is_active = Column(bool, default=False, nullable=False)
    is_blocked = Column(bool, default=False, nullable=False)
