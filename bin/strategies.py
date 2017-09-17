"""Given model predictions and current assets, make new orders (bids?)."""

import numpy as np

def constant_bid_strategy(predictions, portfolio):
    """Return list of bid actions. Can be empty."""
    # Pick a ticker based on prediction magnitude
    keys, values = zip(*((key, p['dimensionless_prediction']) for key, p in predictions.items()))
    i = np.argmax(np.abs(values))
    ticker = keys[i]
    value = values[i]
    # Pick quantity
    quantity = 1
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