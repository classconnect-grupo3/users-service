from sqlalchemy import Column, String, Float
from sqlalchemy import Column, String, Float, Boolean 

from app.database.db import Base


class User(Base):
    __tablename__ = "users"

    uid = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, default=None, nullable=True)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, default=None, nullable=True)
    latitude = Column(Float, default=None, nullable=True)
    longitude = Column(Float, default=None, nullable=True)
    is_active = Column(Boolean, default=False, nullable=False)
    is_blocked = Column(Boolean, default=False, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)

