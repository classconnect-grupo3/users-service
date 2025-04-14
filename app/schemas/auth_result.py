from typing import Optional

from pydantic import BaseModel


class AuthResult(BaseModel):
    id_token: str
    user_location: Optional[str] = None
