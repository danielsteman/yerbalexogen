from backend import crud
from backend import models
from backend.config import AUTH_URL, CLIENT_ID, CLIENT_SECRET, SCOPE, TOKEN_URL
from backend.db import engine, get_db
from backend.utils import create_code_challenge, create_code_verifier
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from requests.auth import HTTPBasicAuth
from sqlalchemy.orm import Session
import json
import requests
import uuid
from backend.routers import router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router)

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


@app.get("/callback")
async def callback(code, db: Session = Depends(get_db)):
    params = {
        "client_id": CLIENT_ID,
        "code": code,
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
    fitbit_token = json.loads(res.content)
    session_id = str(uuid.uuid4())
    fitbit_token["session_id"] = session_id
    db_token = models.FitbitToken(**fitbit_token)
    crud.crud_fitbit_token.create(db, db_token)
    return db_token


@app.get("/token")
async def get_token(session_id: str, db: Session = Depends(get_db)):
    return crud.crud_fitbit_token.get(db, session_id)
