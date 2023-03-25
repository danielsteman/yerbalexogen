from fastapi import APIRouter, Depends, HTTPException
from backend.config import GET_HRV_SUMMARY_BY_DATE
from backend import crud
import httpx
from sqlalchemy.orm import Session
import time

from backend.db import get_db


router = APIRouter(prefix="/data")


@router.get("/hrv-bulk")
def get_hrv_bulk(session_id: str, db: Session = Depends(get_db)):
    token = crud.crud_fitbit_token.get(db, session_id)
    if not token:
        raise HTTPException(status_code=404, detail="Session not found")

    # Check if token is expired > use refresh token

    with httpx.Client() as client:
        headers = {"Authorization": f"Bearer {token.access_token}"}
        r = client.get(
            GET_HRV_SUMMARY_BY_DATE(token.user_id, "2023-01-01"), headers=headers
        )
        return r.content
