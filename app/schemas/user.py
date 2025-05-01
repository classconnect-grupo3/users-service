from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    name: str
    surname: str
    email: EmailStr
    password: str


# Updated Pydantic model for returning user data
class UserRegisterResponseData(BaseModel):
    surname: str
    uid: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    email: EmailStr
    name: str


class UserRegisterResponse(BaseModel):
    data: UserRegisterResponseData


class UserProfileData(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    email: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    model_config = {"from_attributes": True}


class UserProfileResponse(BaseModel):
    data: UserProfileData

class UsersSearchResponse(BaseModel):
    data: list[UserProfileData]
    