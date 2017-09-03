"""
Download, store and read time series data.
Data directory is relative to this file.
"""

import pandas as pd
import os
import pandas_datareader.data as web
from datetime import datetime

dir_path = os.path.dirname(os.path.realpath(__file__))
DIR = os.path.abspath(os.path.join(dir_path, '../data/price_timeseries/'))

def closure_series_from_web(name, start, end):
    """Fetch closure data in a Pandas series.

    Arguments:
    name        The financial instrument name
    """
    df = web.DataReader(name, 'google', start, end, retry_count=3, pause=0.001)
    return df['Close']

def closure_series(name, start=None, end=None, fetcher=closure_series_from_web):
    start, end = (pd.to_datetime(v) for v in (start, end))
    if os.path.exists(name):
        df = read_closure_series(name)
        parts = parts_to_fetch(df, start, end)
        new_dfs = [fetcher(name, s, e) for s, e in parts]
        df = pd.concat([df] + new_dfs).sort_index()
    else:
        df = fetcher(name, start, end)
    to_csv(df, name)
    return df.asfreq('D')

def parts_to_fetch(df, start=None, end=None):
    """Generate tuples defining the ranges to fetch for given existing pandas object."""
    if start is None or start < df.index[0]:
        yield start, df.index[0]
    if end is None or end > df.index[-1]:
        yield df.index[-1], end

def read_closure_series(name):
    """Read from file."""
    return pd.read_csv(closure_series_path(name), index_col=0, parse_dates=True, squeeze=True)

def to_csv(df, name):
    prepare_directory(DIR)
    df.to_csv(closure_series_path(name), header=True)

def prepare_directory(dir_):
    try:
        os.makedirs(dir_)
    except OSError:
        pass

def closure_series_path(name):
    """Return string of path corresponding to given instrument."""
    return os.path.join(DIR, '%s.csv'%name)

def remove_file(name):
    os.remove(closure_series_path(name))

def clear_data():
    for fname in os.listdir(DIR):
        os.remove(os.path.join(DIR, fname))