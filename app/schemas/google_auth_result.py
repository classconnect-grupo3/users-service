from pydantic import BaseModel


class GoogleAuthResult(BaseModel):
    id_token: str
    was_already_registered: bool
