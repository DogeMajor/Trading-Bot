
import pandas as pd
from datetime import datetime
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../bin')))
import timeseries_data

def test_closure_series_path():
    path = timeseries_data.closure_series_path('abc')
    path_should_be = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../data/price_timeseries', 'abc.csv'))
    assert(path==path_should_be)

def test_read_closure_series_nofile():
    series = pd.Series([1.0, 2.0], index=[datetime(2012, 1, 1), datetime(2012, 1, 2)])
    series.name = 'Close'
    df = timeseries_data.closure_series('AAPL', fetcher=lambda name, start, end: series)
    assert(df.equals(series))

# def test_read_closure_series_prepend():
#     series = pd.Series([1.0, 2.0], index=[datetime(2012, 1, 1), datetime(2012, 1, 2)])
#     series.to_csv(series, 'ABCD', header=True)
#     prependable = pd.Series([1.0, 2.0], index=[datetime(2012, 1, 2), datetime(2012, 1, 3)])
#     series.name = 'Close'
#     df = timeseries_data.closure_series('AAPL', fetcher=lambda name, start, end: series)
#     assert(df.equals(series))