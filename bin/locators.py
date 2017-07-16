#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from credentials import username, password


class LoginPageLocators(object):
    def __init__(self):
        self.URL = 'https://www.wallstreetsurvivor.com/login'
        self.USERNAME_FIELD = (By.XPATH, "//input[@id='LoginModel_UserName']")
        self.PASSWORD_FIELD = (By.XPATH, "//input[@id='LoginModel_Password']")
        self.LOGIN_BUTTON = (By.ID, "login_btn")
        self.USERNAME = username  #  From credentials.py
        self.PASSWORD = password  #  From credentials.py

class TradingPageLocators(object):
    def __init__(self):
        self.URL = 'https://www.wallstreetsurvivor.com/play/trade'
        self.TICKER_FIELD = (By.XPATH, "//input[@id='stock_trade_search_field']")
        self.SELECT_ACTION_FIELD = (By.CSS_SELECTOR, "div.icon-arrow-down")
        self.LOGIN_BUTTON = (By.ID, "login_btn")
