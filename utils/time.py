import numpy as np
from datetime import datetime
from datetime import timedelta


def numpy_ts_to_datetime(np_datetime64):
    return datetime.utcfromtimestamp(np_datetime64.astype(datetime) * 1e-9)


def get_next_working_day(input_datetime):
    py_date = input_datetime + timedelta(days=1)  # add 1 day

    # if the date is on the weekend than add until next business day
    # note: weekdays are [0, 1, ... 6]
    while py_date.weekday() in [5, 6]:
        py_date = py_date + timedelta(days=1)

    # return next working day
    return py_date
