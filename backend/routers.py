from fastapi import APIRouter, Depends, HTTPException
from backend.config import GET_HRV_INTRADAY_BY_INTERVAL
from backend import crud
import httpx
from sqlalchemy.orm import Session
import json
import datetime

from backend.db import get_db
from backend.utils import get_dates_in_between


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

    dates = get_dates_in_between(start_date, end_date)
    print(f"between {start_date} and {end_date} are {dates}")

    try:
        with httpx.Client() as client:
            headers = {"Authorization": f"Bearer {token.access_token}"}
            data = []
            for date in dates:
                print(date)
                r = client.get(
                    GET_HRV_INTRADAY_BY_INTERVAL(token.user_id, str(date), str(date)),
                    headers=headers,
                )
                if r.status_code != 200:
                    raise HTTPException(r.status_code, r.content)
                data.append(json.loads(r.content))
            return data
    except Exception:
        raise
