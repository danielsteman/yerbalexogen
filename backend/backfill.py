import httpx
import time
import json
from backend import crud
from backend import schemas
from backend.config import GET_HRV_INTRADAY_BY_INTERVAL, CLIENT_ID
from backend.db import SessionLocal
from backend.utils import get_dates_in_between
import datetime

session_id = "afad5e32-b6f1-496a-87bb-1763d59b3cea"

start_date = datetime.date(2022, 1, 1)
end_date = datetime.date(2022, 1, 2)
db_session = SessionLocal()
dates = get_dates_in_between(start_date, end_date)
token = crud.crud_fitbit_token.get(db_session, session_id)

headers = {"Authorization": f"Bearer {token.access_token}"}

with httpx.Client() as client:
    r = client.get(
        GET_HRV_INTRADAY_BY_INTERVAL(token.user_id, str(start_date), str(end_date)),
        headers=headers,
    )
    days = json.loads(r.content)["hrv"]

for day in days:
    for minute in day["minutes"]:
        crud.crud_hrv_minute.create(
            db_session,
            schemas.HRVMinute(minute=minute["minute"], value=str(minute["value"])),
        )
