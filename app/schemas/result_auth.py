from typing import Optional, Dict
from pydantic import BaseModel


class UserInfo(BaseModel):
    uid: str
    name: str
    surname: str
    is_admin: bool
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class AuthResult(BaseModel):
    id_token: str
    user_info: UserInfo