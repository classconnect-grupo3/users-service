from typing import Optional, List
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
    uid: str
    name: str
    surname: str
    email: EmailStr
    phone: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    is_active: bool = False
    is_blocked: bool = False
    is_admin: bool = False

    model_config = {"from_attributes": True}


class UserProfileResponse(BaseModel):
    data: UserProfileData


class UsersSearchResponse(BaseModel):
    data: list[UserProfileData]


class UsersBatchRequest(BaseModel):
    user_ids: List[str]


# This class is used to update user profile information.
# It is not used for other purposes.
class UserProfileUpdate(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    is_active: Optional[bool] = None
    is_blocked: Optional[bool] = None
    is_admin: Optional[bool] = None

    model_config = {"from_attributes": True}
