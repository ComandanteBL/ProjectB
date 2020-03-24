from datetime import datetime
from datetime import timedelta
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgresql://script:pbscript@localhost:5432/project_b')


def get_stock_data(symbol, start, end, unit):
    df = pd.read_sql_query(
        f"""SELECT * FROM data WHERE
            "symbol"='{symbol}' AND "date" >= '{start}' AND "date" <= '{end}' AND "unit" = '{unit}'
            ORDER BY "date" ASC
        """, engine)
    return df


def get_next_working_day(input_datetime):
    py_date = input_datetime + timedelta(days=1)  # add 1 day

    # if the date is on the weekend than add until next business day
    # note: weekdays are [0, 1, ... 6]
    while py_date.weekday() in [5, 6]:
        py_date = py_date + timedelta(days=1)

    # return next working day
    return py_date