from Crawler.browser import Browser
import pandas as pd
import time

# init browser with yahoo search
browser = Browser()

params = ['BMW.DE']

for p in params:
    # price = browser.get_stock_price(p)
    # eps = browser.get_eps_ttm(p)
    # print(f"Cijena \"{p}\": {price}")
    # print(f"EPS TTM \"{p}\": {eps}")

    historical_data = browser.get_historical_data(p)


    print(1)

print('\U0001F608')
time.sleep(500)