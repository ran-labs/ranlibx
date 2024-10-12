from pydantic import BaseModel


class AuthToken(BaseModel):
    token: str
    # expires_in_secs: int
