from fastapi import FastAPI
from backend.config import AUTH_URL, CLIENT_ID, SCOPE
from backend.utils import create_code_challenge
import requests


app = FastAPI()


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
