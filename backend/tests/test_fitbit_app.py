from typing import Generator
import datetime
import pytest
from sqlalchemy.orm import Session
import uuid
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend import models
from backend.crud import crud_fitbit_token
from backend.crud import crud_hrv_minute

from backend.db import Base
from backend.main import app, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///backend/test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(scope="session")
def db() -> Generator:
    yield TestingSessionLocal()


def test_crud_fitbit_token(db: Session) -> None:
    session_id = str(uuid.uuid4())
    db_obj = models.FitbitToken(
        session_id=session_id,
        access_token="abc",
        expires_in=420,
        refresh_token="tokentoken",
        scope="user",
        token_type="code",
        user_id="useruser",
    )
    crud_fitbit_token.create(db, db_obj)
    new_token = crud_fitbit_token.get(db, session_id)
    assert new_token.session_id == session_id


def test_crud_minute(db: Session) -> None:
    minute = str(datetime.datetime.now())
    value = "some data"
    db_obj = models.HRVMinute(minute=minute, value=value)
    new_minute = crud_hrv_minute.create(db, db_obj)
    assert new_minute.minute == minute
    assert new_minute.value == value
