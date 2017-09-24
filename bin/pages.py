#!/usr/bin/env python

from __future__ import unicode_literals
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from locators import LoginPageLocators, TradingPageLocators, PortfolioPageLocators
from credentials import username, password
import time
import regex as re

class BasePage(object):

    def __init__(self, driver, waiting_time):
        self.driver = driver
        self.driver.set_window_size(1920, 1080)
        self.url = None
        self.waiting_time = waiting_time

    def open_page(self):
        self.driver.get(self.url)

    def page_title(self):
        return self.driver.title

    def find_element(self, *args): # A tuple of arguments, for example of the type (By.ID, 'Hola!')
        return self.driver.find_element(*args)

    def find_element_and_wait(self, waiting_time, *args): # A tuple of arguments, for example of the type (By.ID, 'Hola!')
        elem = WebDriverWait(self.driver, waiting_time).until(EC.presence_of_element_located(*args))
        return elem

    def enter_to_field(self, information, *args):
        elem = self.find_element_and_wait(self.waiting_time, *args)
        elem.send_keys(information)

    def enter_to_field_and_submit(self, information, *args):
        elem = self.find_element_and_wait(self.waiting_time, *args)
        elem.send_keys(information)
        elem.submit()

    def _submit(self, element):  #Prolly not needed
        element.submit()

    def click_element(self, *args):
        elem = self.find_element(*args)
        elem.click()

    def click_element_and_wait(self, time, *args):
        elem = self.find_element_and_wait(time, *args)
        elem.click()

class LoginPage(BasePage):

    def __init__(self, driver, waiting_time=5):
        super(LoginPage, self).__init__(driver, waiting_time)
        self.url = LoginPageLocators.URL
        # print('login', self.waiting_time)

    def login(self):
        self.enter_to_field(LoginPageLocators.USERNAME, LoginPageLocators.USERNAME_FIELD)
        self.enter_to_field_and_submit(LoginPageLocators.PASSWORD, LoginPageLocators.PASSWORD_FIELD)

    def logout(self):
        self.driver.get('https://www.wallstreetsurvivor.com/logout')

class TradingPage(BasePage):
    actions_dict = {'buy': TradingPageLocators.BUY_BUTTON, 'sell': TradingPageLocators.SELL_BUTTON,
    'short': TradingPageLocators.SHORT_BUTTON, 'cover': TradingPageLocators.COVER_BUTTON}

    def __init__(self, driver, waiting_time=5):
        super(TradingPage, self).__init__(driver, waiting_time)
        self.url = TradingPageLocators.URL
        # print('trade', self.waiting_time)

    def _enter_ticker(self, ticker):
        self.enter_to_field(ticker, TradingPageLocators.TICKER_FIELD)
        time.sleep(self.waiting_time)
        self.click_element_and_wait(self.waiting_time, TradingPageLocators.TICKER_DROPDOWN)
        time.sleep(self.waiting_time)

    def _select_action(self, action):
        time.sleep(self.waiting_time)
        self.click_element_and_wait(5, TradingPageLocators.TRADE_MENU)
        time.sleep(self.waiting_time)
        self.click_element_and_wait(self.waiting_time, TradingPage.actions_dict[action])
        time.sleep(self.waiting_time)

    def _enter_no_of_shares(self, amount):
        self.enter_to_field(amount, TradingPageLocators.NUMBER_OF_SHARES_FIELD)
        time.sleep(self.waiting_time)

    def trade(self, ticker, action, amount):
        self._enter_ticker(ticker)
        self._select_action(action)
        self._enter_no_of_shares(amount)
        self.click_element_and_wait(self.waiting_time, TradingPageLocators.TRADE_BUTTON)

    def get_price(self, ticker):
        self._enter_ticker(ticker)
        price_elem = self.find_element(*TradingPageLocators.PRICE_TEXT)
        price_text = price_elem.text
        assert(price_text.startswith('$'))
        price_without_units = price_text.lstrip('$')
        trimmed_price_text = price_without_units.rstrip(' /Share')
        return float(trimmed_price_text)

    def logout(self):
        self.driver.get('https://www.wallstreetsurvivor.com/logout')

class PortfolioPage(BasePage):

    def __init__(self, driver, waiting_time=5):
        super(PortfolioPage, self).__init__(driver, waiting_time)
        self.url = PortfolioPageLocators.URL

    def get_portfolio(self):
        portfolio = []
        time.sleep(self.waiting_time)
        tickers = self.driver.find_elements(*PortfolioPageLocators.TICKER_TABLE)
        for ticker in tickers:
            portfolio.append(self._extract_ticker_information(ticker))
        return portfolio

    def _extract_ticker_information(self, element):
        ticker_id = element.get_attribute('id')
        name = re.findall(r"[^,|' ]+|[,|']", ticker_id)[4]
        attributes = element.find_elements(*PortfolioPageLocators.TICKER_ATTRIBUTES)
        quantity = attributes[1].text
        price_paid = attributes[2].text
        market_value = attributes[4].text
        return {'name': name, 'quantity': quantity, 'price_paid': price_paid, 'market_value': market_value}
