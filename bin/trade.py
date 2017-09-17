
import numpy as np
import pandas as pd
from sequential_model import SequentialModel
from ui import UI
from strategies import constant_bid_strategy

def ticker_group():
    """This should be handled by StockSelector"""
    return ['GOOG', 'AAPL', 'AMZN', 'MSFT', 'NVDA', 'INTC']

def portfolio_dict(portfolio):
    """Portfolio scraped from UI in a cleaned dictionary format."""
    d = {p['name']: {n: v for n, v in p.items() if n!='name'} for p in portfolio}
    for n, subdict in d.items():
        subdict['quantity'] = float(subdict['quantity'])
        subdict['price_paid'] = float(subdict['price_paid'].lstrip('$').replace(',', ''))
    return d

print('Compile model')

model_container = SequentialModel(verbosity=0)

print('Fit model')

predictions = {ticker: model_container.predict(ticker) for ticker in ticker_group()}
print('-----\n', pd.DataFrame(predictions), '\n------')

# df = pd.read_csv('trade_log.csv', parse_dates=True, index_col=0)

print('Open user interface')

ui = UI()
portfolio = ui.get_portfolio()

print('Strategy')

pf_dict = portfolio_dict(portfolio)
bids = constant_bid_strategy(predictions, pf_dict)

print('Apply bids: ', bids)

for bid in bids:
    ui.trade(*bid)