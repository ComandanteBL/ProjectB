import pandas_datareader as web
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
import time

from utils.queries import save_historical_data

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
    t1 = time.time()
    print(f'getting the data for stock: {stocks[i]}')
    hist_data = web.DataReader(stocks[i], data_source='yahoo', start='2020-03-21', end='2020-03-25')
    hist_data.reset_index(level=0, inplace=True)
    print('saving to database...')
    save_historical_data(hist_data, stocks[i])

    t2 = time.time()
    diff = round(t2-t1, 3)
    print(f'=========== DONE {i+1} / {len(stocks)} in {diff:.3f} secs ===========')


