from pydantic import BaseModel


class TokenCreate(BaseModel):
    code: str
