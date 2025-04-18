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
    location: None
    email: EmailStr
    name: str


class UserRegisterResponse(BaseModel):
    data: UserRegisterResponseData

