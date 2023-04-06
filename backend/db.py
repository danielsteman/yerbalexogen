from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, as_declarative
from sqlalchemy.ext.declarative import declared_attr

SQLALCHEMY_DATABASE_URL = "sqlite:///backend/fitbit_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@as_declarative()
class Base(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
