from typing import Optional
from pydantic import BaseModel


class AuthResult(BaseModel):
    id_token: str
    user_location: Optional[str] = None

    class Config:
        schema_extra = {
            "examples": [
                {
                    "id_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    "user_location": "Argentina",
                },
                {
                    "id_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    "user_location": None,
                },
            ],
        }
