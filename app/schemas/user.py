from pydantic import BaseModel, EmailStr
from typing import Optional


class UserBase(BaseModel):
    name: str
    surname: str
    email: EmailStr
    password: str


# Updated Pydantic model for returning user data
class UserRegisterResponseData(BaseModel):
    surname: str
    uid: str
    location: None
    email: EmailStr
    name: str


class UserRegisterResponse(BaseModel):
    data: UserRegisterResponseData

class UserProfileData(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    email: Optional[str] = None 
    location: Optional[str] = None

    model_config = {
        "from_attributes": True  
    }

class UserProfileResponse(BaseModel):
    data: UserProfileData