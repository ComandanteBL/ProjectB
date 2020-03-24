from crawler.browser import Browser
import pandas as pd
from sqlalchemy import create_engine
import time

# init browser with yahoo search
browser = Browser()

# stock symbols

params = ['BMW.DE', 'AAPL', 'MSFT']

engine = create_engine('postgresql://script:pbscript@localhost:5432/project_b')


def save_historical_data(csv):
    df = csv[['Date', 'Close']]
    df = df.rename(columns={"Date": "date", "Close": "value"})  # renaming columns
    df['symbol'] = pd.Series(p, index=df.index)  # add symbol
    df['unit'] = pd.Series('price', index=df.index)  # add symbol

    # new order of columns, dropping NaNs and rounding all int columns to 3 decimal places
    df1 = df[['symbol', 'date', 'value', 'unit']][df['value'].notnull()].round(3)

    # save it to database
    try:
        df1.to_sql('data', engine, if_exists='append', index=False)
    # use the generic Exception, IntegrityError caused trouble
    except Exception as e:
        print("FAILURE TO APPEND: {}".format(e))

    return True


for p in params:
    # price = browser.get_stock_price(p)
    # eps = browser.get_eps_ttm(p)

    hist_data = browser.get_historical_data(p)  # csv loaded into data frame
    save_historical_data(hist_data)

print('\U0001F608')
time.sleep(500)
