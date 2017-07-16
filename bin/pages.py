#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators import LoginPageLocators, TradingPageLocators
from credentials import username, password

class BasePage(object):

    def __init__(self, driver):
        self.driver = driver
        self.url = None

    def open_page(self):
        self.driver.get(self.url)

    def page_title(self):
        return self.driver.title

    def find_element(self, *args): # A tuple of arguments, for example of the type (By.ID, 'Hola!')
        return self.driver.find_element(*args)

    def submit_to_field(self, information, *args):
        elem = self.find_element(*args)
        elem.send_keys(information)
        elem.submit()

    def click_element(self, *args):
        elem = self.find_element(*args)
        elem.click()

class LoginPage(BasePage):

    def __init__(self, driver):
        super(LoginPage, self).__init__(driver)
        #BasePage.__init__(driver)
        self.url = LoginPageLocators.URL
        self.open_page()

    def login(self):
        self.submit_to_field(LoginPageLocators.USERNAME_FIELD, LoginPageLocators.USERNAME)
        self.submit_to_field(LoginPageLocators.PASSWORD_FIELD, LoginPageLocators.PASSWORD)
        self.click_element(LoginPageLocators.LOGIN_BUTTON)


    def logout(self):
        self.driver.get('https://www.wallstreetsurvivor.com/logout')

class TradingPage(BasePage):

    def __init__(self, driver):
        super(TradingPage, self).__init__(driver)
        #BasePage.__init__(driver)
        self.url = TradingPageLocators.URL
        self.open_page()

    def trade(self):
        self.submit_to_field(LoginPageLocators.USERNAME_FIELD, LoginPageLocators.USERNAME)
        self.submit_to_field(LoginPageLocators.PASSWORD_FIELD, LoginPageLocators.PASSWORD)
        self.click_element(LoginPageLocators.LOGIN_BUTTON)

    def logout(self):
        self.driver.get('https://www.wallstreetsurvivor.com/logout')
