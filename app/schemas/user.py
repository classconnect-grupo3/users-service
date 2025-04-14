from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    name: str
    surname: str
    email: EmailStr
    password: str


# Updated Pydantic model for returning user data
class UserResponseData(BaseModel):
    surname: str
    uid: str
    location: Optional[str] = None  # Location can be null
    email: EmailStr
    name: str


class UserResponse(BaseModel):
    data: UserResponseData
