import asyncio
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


def _format(response: httpx.Response):
    data = json.loads(response.content)
    return data["hrv"]


@router.get("/hrv-bulk")
async def get_hrv_bulk(
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
    headers = {"Authorization": f"Bearer {token.access_token}"}

    with httpx.AsyncClient() as client:
        headers = {"Authorization": f"Bearer {token.access_token}"}
        result = []
        for date in dates:
            print(date)
            r = client.get(
                GET_HRV_INTRADAY_BY_INTERVAL(token.user_id, str(date), str(date)),
                headers=headers,
            )
            result.append(_format(r))

    # async def get(date, client):
    #     try:
    #         async with client.get(
    #             GET_HRV_INTRADAY_BY_INTERVAL(token.user_id, str(date), str(date)),
    #             headers=headers,
    #         ) as response:
    #             resp = await response.read()
    #             print(
    #                 "Successfully got url {} with resp of length {}.".format(
    #                     date, len(resp)
    #                 )
    #             )
    #     except Exception as e:
    #         raise

    # async with httpx.AsyncClient() as client:
    #     result = await client.get(
    #         GET_HRV_INTRADAY_BY_INTERVAL(token.user_id, str(dates[0]), str(dates[0])),
    #         headers=headers,
    #     )
    # result = await get(dates[0], client)
    # result = await asyncio.gather(*[get(date, client) for date in dates])

    return result
