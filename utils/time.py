import numpy as np
from datetime import datetime
from datetime import timedelta


def numpy_ts_to_datetime(np_datetime64):
    return datetime.utcfromtimestamp(np_datetime64.astype(datetime) * 1e-9)
