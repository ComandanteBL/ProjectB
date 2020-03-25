from crawler.browser import Browser
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import time

# init browser with yahoo search
from utils.queries import save_historical_data, save_df_to_db

browser = Browser()
engine = create_engine('postgresql://script:pbscript@localhost:5432/project_b')

stocks = [
    'MMM',  # 3M
    'AXP',  # American Express
    'AAPL',  # Apple Inc.
    'BA',  # Boeing
    'CAT',  # Caterpillar Inc.
    'CVX',  # Chevron Corporation
    'CSCO',  # Cisco Systems
    'KO',  # The Coca-Cola Company
    'DOW',  # Dow Inc.
    'XOM',  # ExxonMobil
    'GS',  # Goldman Sachs
    'HD',  # The Home Depot
    'IBM',  # IBM
    'INTC',  # Intel
    'JNJ',  # Johnson & Johnson
    'JPM',  # JPMorgan Chase
    'MCD',  # McDonald's
    'MRK',  # Merck & Co.
    'MSFT',  # Microsoft
    'NKE',  # Nike
    'PFE',  # Pfizer
    'PG',  # Procter & Gamble
    'TRV',  # The Travelers Companies
    'UNH',  # UnitedHealth Group
    'UTX',  # United Technologies
    'VZ',  # Verizon
    'V',  # Visa Inc.
    'WMT',  # Walmart
    'WBA',  # Walgreens Boots Alliance
    'DIS',  # The Walt Disney Company
]

for i in range(0, len(stocks)):
    # price = browser.get_stock_price(p)
    # eps = browser.get_eps_ttm(p)

    eps_ttm = browser.get_eps_ttm(stocks[i])
    d = {'symbol': [stocks[i]], 'date': [datetime.today().date()], 'value': [eps_ttm], 'unit': ['eps_ttm']}
    df = pd.DataFrame(data=d)
    save_df_to_db(df)
    print(f'saved eps_ttm for: {stocks[i]}')
    print(f'=========== DONE {i + 1} / {len(stocks)} ===========')

    # save_historical_data(hist_data, s)

print('\U0001F608')
time.sleep(500)
