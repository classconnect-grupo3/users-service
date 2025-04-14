from sqlalchemy import Column, String

from app.database.db import Base


class User(Base):
    __tablename__ = "users"

    uid = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False)
    location = Column(String, unique=True, nullable=True)
