#!/usr/bin/env python

from selenium import webdriver
from trader import Trader
#from credentials import username, password
import tensorflow as tf
import time
from trading_adviser import TradingAdviser

class StockSelector(object):
    """Hand-picked tickers."""
    def __init__(self):
        self.tickers = [
            'GOOG', 'AAPL', 'AMZN', 'MSFT', 'NVDA', 'INTC']
    def select(self, *args):
        return self.tickers

class Bot(object):

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.trader = Trader(self.driver, 3)
        self.trader.login()
        self.stock_selector = StockSelector()
        self.trading_adviser = TradingAdviser(self.trader)

    def trade(self):
        # Pick instruments
        tickers = self.stock_selector.select()
        # Find a subset to trade with
        suggestions = self.trading_adviser.suggest(tickers)
        # Trade
        self.trader.open_trading_page()
        for suggestion in suggestions:
            self.trader.trade(*suggestion)

    def __del__(self):
        self.trader.logout()
        self.driver.close()

if __name__=='__main__':
    bot = Bot()
    portfolio = bot.trader.get_portfolio()
    print('Current portfolio', portfolio)
    bot.trade()
