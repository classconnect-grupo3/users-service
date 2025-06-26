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

    model_config = {"from_attributes": True}


# Admin metrics schemas
class UserStatsData(BaseModel):
    total_users: int
    active_users: int
    inactive_users: int
    blocked_users: int
    admin_users: int
    users_with_phone: int
    users_without_phone: int
    users_with_location: int
    users_without_location: int


class UserStatsResponse(BaseModel):
    data: UserStatsData


class UserIsActiveResponse(BaseModel):
    is_active: bool


class UserIsAdminResponse(BaseModel):
    is_admin: bool
    email: str
