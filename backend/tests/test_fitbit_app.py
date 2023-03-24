import uuid
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend import models
from backend.crud import crud_fitbit_token

from backend.db import Base
from backend.main import app, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_test_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_crud_fitbit_token():
    session_id = str(uuid.uuid4())
    test_db_session = get_test_db()
    db_obj = models.FitbitToken(
        session_id=session_id,
        access_token="abc",
        expires_in=420,
        refresh_token="tokentoken",
        scope="user",
        token_type="code",
        user_id="useruser",
    )
    crud_fitbit_token.create(test_db_session, db_obj)
    new_token = crud_fitbit_token.get(test_db_session, session_id)
    assert new_token.session_id == session_id
