import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import pandas as pd


class Browser:
    driver = webdriver.Chrome('../driver/chromedriver_80.exe')  # Optional argument, if not specified will search path.

    def __init__(self):
        self.url = 'https://finance.yahoo.com/'
        self.driver.get(self.url)
        self.driver.find_element_by_name('agree').click()  # click on ok
        search_box = self.driver.find_element_by_name('yfin-usr-qry')  # get search field
        search_box.send_keys('BMW.DE')  # insert stock name
        time.sleep(1)  # wait for instant search
        search_box.submit()  # submit search query
        # time.sleep(2)  # wait for page load

    def get_stock_price(self):
        try:
            WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_id("quote-header-info"))  # wait for load
            price_line = self.driver.find_element_by_id("quote-header-info").text.split("\n")[3]  # get element
            sign = price_line.split('(')[1][:1]  # parse sign (+/-)
            stock_price = float(price_line.split(sign)[0])  # parse price
            return stock_price
        except NotImplementedError:
            return None

    def get_eps_ttm(self):
        try:
            WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_id("quote-header"))  # wait for load
            value = self.driver.find_element_by_id("quote-header").text.split('\n')[13].split(' ')[-1]  # get element
            eps_ttm = float(value)
            return eps_ttm
        except NotImplementedError:
            return None


browser = Browser()
price = browser.get_stock_price()
eps = browser.get_eps_ttm()
print(f"Cijena: {price}")
print(f"EPS TTM: {eps}")
print('\U0001F608')

time.sleep(500)
