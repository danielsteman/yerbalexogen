from backend.db import Base
from sqlalchemy import Column, DateTime, String, Integer
from sqlalchemy.sql import func


class FitbitToken(Base):
    # created = Column(DateTime, default=func.now())
    session_id = Column(String, primary_key=True)
    access_token = Column(String)
    expires_in = Column(Integer)
    refresh_token = Column(String)
    scope = Column(String)
    token_type = Column(String)
    user_id = Column(String)
