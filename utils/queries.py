import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgresql://script:pbscript@localhost:5432/project_b')


def save_historical_data(csv, s):
    df = csv[['Date', 'Close']]
    df = df.rename(columns={"Date": "date", "Close": "value"})  # renaming columns
    df['symbol'] = pd.Series(s, index=df.index)  # add symbol
    df['unit'] = pd.Series('price', index=df.index)  # add symbol
    save_df_to_db(df)


def save_df_to_db(df):
    # df needs to have ['symbol', 'date', 'value', 'unit']

    # new order of columns, dropping NaNs and rounding all int columns to 3 decimal places
    df1 = df[['symbol', 'date', 'value', 'unit']][df['value'].notnull()].round(3)

    # save it to database
    try:
        df1.to_sql('hist_data', engine, if_exists='append', index=False)
    # use the generic Exception, IntegrityError caused trouble
    except Exception as e:
        print("FAILURE TO APPEND: {}".format(e))

    return True


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
