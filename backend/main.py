import json
from backend import models
import requests
from backend.config import AUTH_URL, CLIENT_ID, CLIENT_SECRET, SCOPE, TOKEN_URL
from backend.db import SessionLocal, engine
from fastapi import FastAPI, Depends, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from requests.auth import HTTPBasicAuth
from sqlalchemy.orm import Session
from backend.utils import create_code_challenge, create_code_verifier
import uuid

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
app.add_middleware(SessionMiddleware, secret_key="some-random-string")
app.state.verifier = create_code_verifier()


@app.get("/login")
async def login(request: Request, response: Response, db: Session = Depends(get_db)):
    # compare cookies in request with session_id in db
    # logged_in = bool(
    #     db.query(models.FitbitToken)
    #     .filter(models.FitbitToken.session_id == request.cookies.get("session_id"))
    #     .first()
    # )
    # print(logged_in)

    params = {
        "client_id": CLIENT_ID,
        "scope": SCOPE,
        "code_challenge": create_code_challenge(app.state.verifier),
        "code_challenge_method": "S256",
        "response_type": "code",
    }
    res = requests.get(f"{AUTH_URL}", params=params)
    # if user has no active session (token is not expired) create new session and set in response cookie
    session_id = str(uuid.uuid4())
    print(f"session_id created at login: {session_id}")
    response.set_cookie(key="session_id", value=session_id)
    return {"url": res.url}


@app.get("/session")
async def session_test(request: Request, response: Response):
    print(request.cookies)
    return request.cookies


@app.get("/session_exists")
async def session_exists(request: Request, db: Session = Depends(get_db)):
    db_obj = (
        db.query(models.FitbitToken)
        .filter(models.FitbitToken.session_id == "0cac45e2-3773-49d5-8261-5d5cb605b381")
        .first()
    )
    all_db_obj = [x for x in db.query(models.FitbitToken).all()]
    return {"db_obj": db_obj, "all_db_obj": all_db_obj, "n_db_obj": len(all_db_obj)}


@app.get("/callback")
async def callback(code, request: Request, db: Session = Depends(get_db)):
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
    print(f"request cookies from callback endpoint: {request.cookies}")
    fitbit_token["session_id"] = request.cookies.get("session_id")

    db_token = models.FitbitToken(**fitbit_token)

    print(f"db_token session_id: {db_token.session_id}")

    # db.add(db_token)
    # db.commit()
    # db.refresh(db_token)

    return db_token
