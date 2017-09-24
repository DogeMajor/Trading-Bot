#!/usr/bin/env python

from selenium.webdriver.common.by import By
from credentials import username, password

class LoginPageLocators(object):

        URL = 'https://www.wallstreetsurvivor.com/login'
        USERNAME_FIELD = (By.ID, 'LoginModel_UserName')
        PASSWORD_FIELD = (By.ID, 'LoginModel_Password')
        LOGIN_BUTTON = (By.ID, "login_btn")  # Not needed when using Chrome
        USERNAME = username  #  From credentials.py
        PASSWORD = password  #  From credentials.py

class TradingPageLocators(object):
        URL = 'https://www.wallstreetsurvivor.com/play/trade'
        TICKER_FIELD = (By.ID, 'stock_trade_search_field')
        TICKER_DROPDOWN = (By.XPATH, "//a[@class='btn' and @href]")
        TRADE_MENU = (By.ID, 'menuTradeAction')
        PRICE_TEXT = (By.CLASS_NAME, 'price')

        BUY_BUTTON = (By.XPATH, "//*[@data-menu-option='buy']/div")
        SELL_BUTTON = (By.XPATH, "//*[@data-menu-option='sell']/div")
        SHORT_BUTTON = (By.XPATH, "//*[@data-menu-option='short']/div")
        COVER_BUTTON = (By.XPATH, "//*[@data-menu-option='cover']/div")

        NUMBER_OF_SHARES_FIELD = (By.ID, 'numberOfShares')
        TRADE_BUTTON = (By.ID, 'tradeTotal')

class PortfolioPageLocators(object):
        URL = 'http://www.wallstreetsurvivor.com/play/portfolio'
        TICKER_TABLE = (By.XPATH, "//tr[@id]")
        TICKER_ATTRIBUTES = (By.TAG_NAME, "td")
