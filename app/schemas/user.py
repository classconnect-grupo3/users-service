from typing import List
import uuid
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    name: str
    surname: str
    email: EmailStr
    password: str
    # phone_number: str
    # isAdmin: bool


# Pydantic model for returning the course data with ID
class User(UserBase):
    id: uuid.UUID

    class Config:
        from_attributes = (
            True  # Tells Pydantic to treat the SQLAlchemy model as a dictionary
        )


class AllUsersResponse(BaseModel):
    data: List[User]


class UserResponse(BaseModel):
    data: User
