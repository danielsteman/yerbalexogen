import base64
import datetime
import hashlib
import os
import re
import math
from typing import List, Literal, Optional


def create_code_verifier() -> str:
    code_verifier = base64.urlsafe_b64encode(os.urandom(40)).decode("utf-8")
    code_verifier = re.sub("[^a-zA-Z0-9]+", "", code_verifier)
    return code_verifier


def create_code_challenge(code_verifier: str) -> str:
    code_challenge = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    code_challenge = base64.urlsafe_b64encode(code_challenge).decode("utf-8")
    code_challenge = code_challenge.replace("=", "")
    return code_challenge


def get_dates_in_between(
    start_date: datetime.date, end_date: datetime.date
) -> Optional[List[datetime.date]]:
    if end_date < start_date:
        return None
    n_days = end_date - start_date
    return [start_date + datetime.timedelta(days=i) for i in range(n_days.days + 1)]


def get_interval(
    start_date: datetime.date,
    end_date: datetime.date,
    chunk_size: int,
    *,
    chunk_unit: Literal["day", "month"] = "day",
):
    if chunk_unit == "month":
        raise NotImplementedError

    days = (end_date - start_date).days
    chunks = math.floor(days / chunk_size)
    remainder = days % chunk_size

    interval_start = start_date
    interval = []
    for _ in range(chunks):
        _interval_end = interval_start + datetime.timedelta(days=chunk_size - 1)
        _interval = (interval_start, _interval_end)
        interval.append(_interval)
        interval_start = _interval_end + datetime.timedelta(days=1)

    if remainder:
        interval.append(
            (interval_start, interval_start + datetime.timedelta(days=remainder))
        )

    return interval


print(get_interval(datetime.date(2022, 1, 1), datetime.date(2022, 3, 15), 30))
