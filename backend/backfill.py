import time
import httpx
import json
from backend import crud
from backend import schemas
from backend.config import GET_HRV_INTRADAY_BY_INTERVAL
from backend.db import SessionLocal
from backend.utils import get_dates_in_between, get_interval
import datetime

session_id = "911719c7-22b3-4d54-aaf4-011b05e25854"

start_date = datetime.date(2022, 1, 1)
end_date = datetime.date(2022, 12, 31)
db_session = SessionLocal()
dates = get_dates_in_between(start_date, end_date)
token = crud.crud_fitbit_token.get(db_session, session_id)

headers = {"Authorization": f"Bearer {token.access_token}"}

for interval in get_interval(start_date, end_date, chunk_size=30):
    with httpx.Client() as client:
        r = client.get(
            GET_HRV_INTRADAY_BY_INTERVAL(
                token.user_id, str(interval[0]), str(interval[1])
            ),
            headers=headers,
        )
        days = json.loads(r.content)["hrv"]
        print(f"N days in interval: {len(days)}")

    time.sleep(0.1)

    inserted_records = 0

    for day in days:
        print(f"N minutes in day: {len(day['minutes'])}")
        for minute in day["minutes"]:
            new_minute = crud.crud_hrv_minute.create(
                db_session,
                schemas.HRVMinute(minute=minute["minute"], value=str(minute["value"])),
            )
            if new_minute:
                inserted_records += 1

    print(f"N inserted: {inserted_records}")
