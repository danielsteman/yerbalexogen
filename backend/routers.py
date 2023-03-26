from fastapi import APIRouter, Depends, HTTPException
from backend.config import GET_HRV_INTRADAY_BY_INTERVAL, GET_HRV_SUMMARY_BY_DATE
from backend import crud
import httpx
from sqlalchemy.orm import Session
import json
import datetime

from backend.db import get_db


router = APIRouter(prefix="/data")


@router.get("/hrv-bulk")
def get_hrv_bulk(
    session_id: str,
    start_date: datetime.date,
    end_date: datetime.date,
    db: Session = Depends(get_db),
):
    if start_date > end_date:
        raise HTTPException(status_code=400, detail="Start date cannot exceed end date")
    token = crud.crud_fitbit_token.get(db, session_id)
    if not token:
        raise HTTPException(status_code=404, detail="Session not found")

    # Check if token is expired > use refresh token

    n_days = end_date - start_date
    dates = [start_date + datetime.timedelta(days=i) for i in range(n_days.days + 1)]

    try:
        with httpx.Client() as client:
            headers = {"Authorization": f"Bearer {token.access_token}"}
            r = client.get(
                GET_HRV_INTRADAY_BY_INTERVAL(token.user_id, "2023-01-01", "2023-03-25"),
                headers=headers,
            )
            if r.status_code != 200:
                raise HTTPException(r.status_code, r.content)
            return json.loads(r.content["data"])
    except Exception as e:
        raise HTTPException(
            500, f"Something went wrong while retrieving Fitbit data. Details: {e}"
        ) from e
