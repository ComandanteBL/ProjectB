import time
import threading
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import re


class Browser:
    # driver chrome version 80
    driver = webdriver.Chrome('../driver/chromedriver.exe')  # Optional argument, if not specified will search path.

    def __init__(self):
        self.url = 'https://finance.yahoo.com/'
        self.driver.get(self.url)
        self.driver.find_element_by_name('agree').click()  # click on ok

    def __get_element_by_id(self, element_id):
        try:
            element = self.driver.find_element_by_id(element_id)
            return element
        except NoSuchElementException:
            return False

    def __loaded(self, symbol):
        quote_header_info = self.__get_element_by_id("quote-header-info")
        match = None
        if quote_header_info:
            match = re.search(f'({symbol})', quote_header_info.text.split("\n")[0])

        if match and quote_header_info:
            # if loaded return immediately
            return
        else:
            # if page was not loaded upon retrieving value, load and then return
            search_box = self.driver.find_element_by_name('yfin-usr-qry')  # get search field
            search_box.send_keys(symbol)  # insert stock name
            time.sleep(1)  # wait for instant search
            search_box.submit()  # submit search query
            return

    def get_stock_price(self, symbol):
        thread = threading.Thread(target=self.__loaded, args=[symbol])
        thread.start()  # starting thread
        thread.join()  # waiting on thread and continuing
        try:
            WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_id("quote-header-info"))  # wait for load
            price_line = self.driver.find_element_by_id("quote-header-info").text.split("\n")[3]  # get element
            sign = price_line.split('(')[1][:1]  # parse sign (+/-)
            stock_price = float(price_line.split(sign)[0])  # parse price
            return stock_price
        except NotImplementedError:
            return None

    def get_eps_ttm(self, symbol):
        thread = threading.Thread(target=self.__loaded, args=[symbol])
        thread.start()  # starting thread
        thread.join()  # waiting on thread to finish and continue
        try:
            WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_id("quote-header"))  # wait for load
            all_text = self.driver.find_element_by_id("quote-header").text  # get element
            match = re.search('EPS \(TTM\) (.*)\n', all_text)
            if match:
                eps_ttm = float(match.group(1))
                return eps_ttm
            else:
                return None
        except NotImplementedError:
            return None

    def get_historical_data(self, symbol):
        # returning DataFrame

        thread = threading.Thread(target=self.__loaded, args=[symbol])
        thread.start()  # starting thread
        thread.join()  # waiting on thread to finish and continue
        try:
            WebDriverWait(self.driver, 10).until(
                lambda x: x.find_element_by_id("quote-header"))  # wait for quote header
            self.driver.find_element_by_css_selector("li[data-test='HISTORICAL_DATA']").click()  # click on hist data

            WebDriverWait(self.driver, 10).until(
                lambda x: x.find_element_by_css_selector("svg[data-icon='CoreArrowDown']"))  # wait for arrow appear
            self.driver.find_element_by_css_selector("svg[data-icon='CoreArrowDown']").click()  # click on arrow

            WebDriverWait(self.driver, 10).until(
                lambda x: x.find_element_by_css_selector("button[data-value='MAX']"))  # wait for max to appear
            self.driver.find_element_by_css_selector("button[data-value='MAX']").click()  # click on max

            self.driver.find_element_by_xpath("//span[.='Apply']").click()  # click on apply button

            # get link to execute
            download_link = self.driver.find_element_by_xpath(".//a[contains(@href,'download')]").get_attribute('href')
            csv = pd.read_csv(download_link)
            return csv
        except NotImplementedError:
            return None
