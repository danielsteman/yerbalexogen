import datetime

from backend.utils import get_dates_in_between, get_interval


def test_get_dates_in_between():
    dates = get_dates_in_between(datetime.date(2022, 1, 1), datetime.date(2022, 1, 3))
    expected = [
        datetime.date(2022, 1, 1),
        datetime.date(2022, 1, 2),
        datetime.date(2022, 1, 3),
    ]
    assert dates == expected


def test_get_dates_in_between_invalid():
    dates = get_dates_in_between(datetime.date(2022, 1, 5), datetime.date(2022, 1, 1))
    assert dates == None


def test_get_interval():
    interval = get_interval(datetime.date(2022, 1, 1), datetime.date(2022, 3, 15), 30)
    assert len(interval) == 3
    interval = get_interval(datetime.date(2022, 1, 1), datetime.date(2022, 1, 15), 30)
    assert len(interval) == 1
