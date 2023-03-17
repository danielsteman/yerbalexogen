from db import Base
from sqlalchemy import Column, String, Integer


class FitbitToken(Base):
    session_id = Column(String)
    access_token = Column(String)
    expires_in = Column(Integer)
    refresh_token = Column(String)
    scope = Column(String)
    token_type = Column(String)
    user_id = Column(String)
