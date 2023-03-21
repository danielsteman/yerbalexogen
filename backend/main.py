import json
from backend import models
import requests
from backend.config import AUTH_URL, CLIENT_ID, CLIENT_SECRET, SCOPE, TOKEN_URL
from backend.db import SessionLocal, engine
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from requests.auth import HTTPBasicAuth
from sqlalchemy.orm import Session
from backend.utils import create_code_challenge, create_code_verifier
from backend import schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


origins = [
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
    "http://localhost:5173",
    "http://localhost:5174",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.verifier = create_code_verifier()


@app.get("/login")
async def login():
    params = {
        "client_id": CLIENT_ID,
        "scope": SCOPE,
        "code_challenge": create_code_challenge(app.state.verifier),
        "code_challenge_method": "S256",
        "response_type": "code",
    }
    res = requests.get(f"{AUTH_URL}", params=params)
    return {"url": res.url}


@app.get("/code_verifier")
async def code_verifier():
    return {"code_verifier": app.state.verifier}


@app.get("/callback")
async def callback(code: schemas.TokenCreate, db: Session = Depends(get_db)):
    params = {
        "client_id": CLIENT_ID,
        "code": code.code,
        "code_verifier": app.state.verifier,
        "grant_type": "authorization_code",
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    res = requests.post(
        TOKEN_URL,
        auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET),
        params=params,
        headers=headers,
    )
    body = json.loads(res.content)
    body["session_id"] = code.session_id

    db_token = models.FitbitToken(**body)
    db.add(db_token)
    db.commit()
    db.refresh(db_token)

    return db_token
