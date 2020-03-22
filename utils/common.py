import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgresql://script:pbscript@localhost:5432/project_b')


def get_stock_data(symbol, start, end, unit):
    df = pd.read_sql_query(
        f"""SELECT * FROM data WHERE
            "symbol"='{symbol}' AND "date" >= '{start}' AND "date" <= '{end}' AND "unit" = '{unit}'

        """, engine)
    return df
