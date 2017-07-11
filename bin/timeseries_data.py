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

def closure_series_from_web(name, start, end):
    """Fetch closure data in a Pandas series.

    Arguments:
    name        The financial instrument name
    """
    df = web.DataReader(name, 'google', start, end, retry_count=3, pause=0.001)
    return df['Close']

def closure_series_path(name):
    """Return string of path corresponding to given instrument."""
    return os.path.join(DIR, '%s.csv'%name)

def to_csv(df, name):
    prepare_directory(DIR)
    df.to_csv(closure_series_path(name), header=True)

def read_closure_series(name):
    """Read from file."""
    return pd.read_csv(closure_series_path(name), index_col=0, parse_dates=True, squeeze=True)

def closure_series(name, start=None, end=None, fetcher=closure_series_from_web):
    start, end = (pd.to_datetime(v) for v in (start, end))
    if os.path.exists(name):
        df = read_closure_series(name)
        append_start = start is not None and start < df.index[0]
        append_end = end is not None and end > df.index[-1]
        if append_start or append_end:
            if append_start:
                newdf = fetcher(name, start, df.index[0])
                df = newdf.append(df)
            if append_end:
                newdf = fetcher(name, df.index[-1], end)
                df = df.append(newdf)
            df = df.drop_duplicates()
    else:
        df = fetcher(name, start, end)
    to_csv(df, name)
    return df.asfreq('D')

def clear_data():
    for fname in os.listdir(DIR):
        os.remove(os.path.join(DIR, fname))