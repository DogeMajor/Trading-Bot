#!/usr/bin/env python

from selenium import webdriver
from pages import LoginPage, TradingPage, PortfolioPage
import time

class Trader(object):

    def __init__(self, driver, waiting_time=5):
        self.driver = driver
        self.login_page = LoginPage(self.driver, waiting_time)
        self.trading_page = TradingPage(self.driver, waiting_time)
        self.portfolio_page = PortfolioPage(self.driver, waiting_time)

    def __del__(self):
        print("Trader destroyed!")

    def login(self):
        self.login_page.open_page()
        self.login_page.login()

    def open_trading_page(self):
        self.trading_page.open_page()

    def logout(self):
        self.trading_page.logout()

    def trade(self, ticker, action, amount):
        self.trading_page.trade(ticker, action, amount)

    def get_price(self, ticker):
        return self.trading_page.get_price(ticker)

    def open_portfolio_page(self):
        self.portfolio_page.open_page()

    def get_portfolio(self):
        self.open_portfolio_page()
        return self.portfolio_page.get_portfolio()

if __name__=='__main__':
    driver = webdriver.Chrome()
    trader = Trader(driver, 3)
    trader.login()
    trader.open_trading_page()
    trader.trade('CCJ', 'buy', 10)
    time.sleep(2)
    trader.open_portfolio_page()
    portfolio = trader.get_portfolio()
    trader.logout()
    driver.close()
    print(portfolio)
