"""
Download, store and read time series data.
Directory is relative to this file.
"""


import pandas as pd
import os
import pandas_datareader.data as web
from datetime import datetime

dir_path = os.path.dirname(os.path.realpath(__file__))
DIR = os.path.abspath(os.path.join(dir_path, '../data/price_timeseries/'))

def prepare_directory(dir_):
    try:
        os.mkdir(dir_)
    except FileExistsError:
        pass

def entire_closure_series_from_web(name):
    """Fetch all closure data in a Pandas series.

    Arguments:
    name        The financial instrument name
    """
    df = web.DataReader(name, 'google', None, datetime.now(), retry_count=3, pause=0.001)
    return df['Close']

def closure_series_path(name):
    """Return string of path corresponding to given instrument."""
    return os.path.join(DIR, '%s.csv'%name)

def fetch_closure_series(name):
    """Download and save series to text file."""
    df = entire_closure_series_from_web(name)
    prepare_directory(DIR)
    df.to_csv(closure_series_path(name))

def read_closure_series(name):
    """Read from file."""
    return pd.read_csv(closure_series_path(name), index_col=0, parse_dates=True, squeeze=True)

def closure_series(name):
    """Closure series from file. If no file, fetch from web."""
    if os.path.exists(name):
        df = read_closure_series(name)
    else:
        fetch_closure_series(name)
        df = read_closure_series(name)
    return df

def clear_data():
    for fname in os.listdir(DIR):
        os.remove(os.path.join(DIR, fname))