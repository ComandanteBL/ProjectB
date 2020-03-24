import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgresql://script:pbscript@localhost:5432/project_b')


def get_stock_data(symbol, start, end, unit):
    df = pd.read_sql_query(
        f"""
            SELECT * FROM "hist_data" WHERE
            "symbol"='{symbol}' AND "date" >= '{start}' AND "date" <= '{end}' AND "unit" = '{unit}'
            ORDER BY "date" ASC
        """, engine)
    return df


def save_model_to_db(model_name, path_string, rmse):
    with engine.connect() as con:
        query = f"""
                INSERT INTO "models" (name, path, rmse) 
                VALUES ('{model_name}', '{path_string}', {rmse});
                """
        con.execute(query)
    return


def load_best_model_from_db(symbol=None, model_type=None):
    df = pd.read_sql_query(
        f"""
            SELECT * FROM "models" WHERE 
            "symbol" = '{symbol}' and
            "type" = '{model_type}'
            ORDER BY "rmse" ASC limit 1;
        """, engine)
    return df
