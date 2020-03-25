import pandas as pd
from utils.queries import get_entry_for_date
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

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

years_backwards = 7  # number of years backwards (7 recommended)
corp_bond_rate = 3.625

last_date = datetime.today().date()
previous_date = (datetime.now() - relativedelta(years=years_backwards)).date()

# stocks = ['MSFT']

d = {
    'stock': [],
    'current price': [],
    'value estimate': [],
    'difference': []
}

for i in range(0, len(stocks)):
    print(stocks[i])
    eps_ttm = get_entry_for_date(stocks[i], last_date, 'eps_ttm')['value'][0]
    last_price = get_entry_for_date(stocks[i], last_date, 'price')['value'][0]
    previous_price = get_entry_for_date(stocks[i], previous_date, 'price')
    if previous_price.shape[0] == 0:
        continue
    else:
        previous_price = previous_price['value'][0]

    price_div = last_price / previous_price
    yearly_growth = round((price_div ** (1 / years_backwards)), 3)

    percent_growth = round((yearly_growth * 100) - 100, 3)

    value_estimation = (eps_ttm * (7 + percent_growth) * 4.4) / corp_bond_rate

    d['stock'].append(stocks[i])
    d['current price'].append(last_price)
    d['value estimate'].append(value_estimation)
    diff = ((float(value_estimation) - last_price) / last_price) * 100
    d['difference'].append(diff)

df = pd.DataFrame(data=d)
print(df)
