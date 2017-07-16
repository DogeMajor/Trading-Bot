#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pages

class Trader(object):

    def __init__(self, driver):
        self.driver = driver
        self.login_page = pages.LoginPage(self.driver)

        self.trading_page = None

    def __del__(self):
        self.driver.quit()
        print("Trader webdriver destroyed!")


    def open_trading_page(self):
        self.login_page.login()
        self.trading_page =  pages.TradingPage(self.driver)

    def logout(self):
        login_page.logout()

    def trade(self, action, ticker, amount, price):
        pass


driver = webdriver.Firefox()
trader = Trader(driver)
trader.open_trading_page()
driver.get_screenshot_as_file('../data/login_trader.png')
trader.logout()
