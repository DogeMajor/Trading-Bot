#!/usr/bin/env python

import math
import numpy as np
import pandas as pd
from keras_model import KerasModel

class TradingAdviser(object):

    def __init__(self, trader):
        self.trader = trader

    def suggest(self, tickers):
        """Suggest bid order for given group of tickers."""

        print('Compile model')

        model_container = KerasModel(verbosity=0)

        print('Fit model')

        predictions = {ticker: model_container.predict(ticker) for ticker in tickers}
        print_dict_as_table(predictions)

        print('Open web driver and fetch data')

        portfolio = self.trader.get_portfolio()

        print('Strategy')

        pf_dict = portfolio_dict(portfolio)
        orders = constant_bid_strategy(predictions, pf_dict, self.trader)

        return orders

def print_dict_as_table(dictionary):
    print('-----\n', pd.DataFrame(dictionary), '\n------')

def portfolio_dict(portfolio):
    """Portfolio scraped from web in a cleaned dictionary format. 
    By cleaning I mean type changes."""
    d = {p['name']: {n: v for n, v in p.items() if n!='name'} for p in portfolio}
    for n, subdict in d.items():
        subdict['quantity'] = float(subdict['quantity'])
        subdict['price_paid'] = float(subdict['price_paid'].lstrip('$').replace(',', ''))
    return d

def constant_bid_strategy(predictions, portfolio, trader):
    """Return list of bid actions. Can be empty."""
    # Pick a ticker based on prediction magnitude
    keys, values = zip(*((key, p['dimensionless_prediction']) for key, p in predictions.items()))
    i = np.argmax(np.abs(values))
    ticker = keys[i]
    value = values[i]
    # Pick quantity
    trader.open_trading_page()
    price = trader.get_price(ticker)
    quantity = math.ceil(1000/price)
    if value > 0:
        action = 'buy'
    elif value < 0:
        if ticker in portfolio and portfolio[ticker]['quantity'] >= quantity:
            action = 'sell'
        else:
            # This may act weird. What if there's already some amount of this asset in portfolio?
            action = 'short'
    else:
        # Unlikely
        return []
    return [(ticker, action, quantity)]