import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from app.database.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=True)
    # email = Column(String, unique=True, nullable=False)
    # password = Column(String, nullable=False)
    # phone = Column(String, nullable=True)
    # isAdmin = Column(bool, nullable=True)
