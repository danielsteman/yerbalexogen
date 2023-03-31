import httpx
import time
import json
from backend import crud
from backend.config import GET_HRV_INTRADAY_BY_INTERVAL, CLIENT_ID
from backend.db import SessionLocal
from backend.utils import get_dates_in_between
import datetime

session_id = None
user_id = CLIENT_ID

start_date = datetime.date(2022, 1, 1)
end_date = datetime.date(2022, 12, 31)
db_session = SessionLocal()
dates = get_dates_in_between(start_date, end_date)
access_token = crud.crud_fitbit_token.get(db_session, session_id)

headers = {"Authorization": f"Bearer {access_token}"}

with httpx.Client() as client:
    r = client.get(
        GET_HRV_INTRADAY_BY_INTERVAL(user_id, str(dates[0]), str(dates[0])),
        headers=headers,
    )
    print(json.loads(r.content))
