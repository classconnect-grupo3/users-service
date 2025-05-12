from typing import Optional, Dict
from pydantic import BaseModel


class AuthResult(BaseModel):
    id_token: str
    user_location: Optional[Dict[str, Optional[float]]] = None
