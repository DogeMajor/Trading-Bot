#!/usr/bin/env python

from selenium import webdriver
from trader import Trader
#from credentials import username, password
import tensorflow as tf
import time

class UI(object):
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.trader = Trader(self.driver, 3)
        self.trader.login()
        self.stockselector = None
        self.stockpredictor = None
        self.portfolio = {}

    def get_portfolio(self):
        self.trader.open_portfolio_page()
        return self.trader.get_portfolio()

    def trade(self, ticker, action, amount):
        self.trader.open_trading_page()
        self.trader.trade(ticker, action, amount)

    def __del__(self):
        self.trader.logout()
        self.driver.close()

if __name__=='__main__':
    ui = UI()
    portfolio = ui.get_portfolio()
    print(portfolio)
