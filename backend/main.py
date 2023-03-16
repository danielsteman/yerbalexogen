from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import AUTH_URL, CLIENT_ID, SCOPE
from utils import create_code_challenge
import requests


app = FastAPI()

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

@app.get("/login")
async def login():
    params = {
        "client_id": CLIENT_ID,
        "scope": SCOPE,
        "code_challenge": create_code_challenge(),
        "code_challenge_method": "S256",
        "response_type": "code",
    }
    res = requests.get(f"{AUTH_URL}", params=params)
    return {"url": res.url}

@app.get("/callback")
async def callback(code: str):
    # save code in db
    return {"status": "received"}