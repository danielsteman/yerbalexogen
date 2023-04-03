from pydantic import BaseModel


class Token(BaseModel):
    session_id: str
    access_token: str
    expires_in: int
    refresh_token: str
    scope: str
    token_type: str
    user_id: str


class HRVMinute(BaseModel):
    minute: str
    value: str
