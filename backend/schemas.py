from pydantic import BaseModel


class TokenCreate(BaseModel):
    session_id: str
    code: str
