
"""
Tests for timeseries_data;
it uses some file I/O but remote server inputs are mocked. 
"""

import numpy as np
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

def mock_fetch(name, start, end):
    """Return a mock pandas.Series, with values 0, 1, 2, ... and datetime index based on input.
    """
    index = pd.date_range(start, end, freq='D')
    series = pd.Series(np.arange(len(index)), index=index)
    return series

def test_closure_series_nofile():
    s0 = mock_fetch('FAKENAME', '2012-01-01', '2012-01-02')
    s1 = timeseries_data.closure_series('FAKENAME', '2012-01-01', '2012-01-02', fetcher=mock_fetch)
    assert(s0.equals(s1))

def test_closure_series_withfile():
    name = 'FAKENAME'
    series = mock_fetch(name, '2012-01-03', '2012-01-05')
    timeseries_data.to_csv(series, name)
    output = timeseries_data.closure_series('FAKENAME', '2012-01-01', '2012-01-04', fetcher=mock_fetch)
    output_should_be = mock_fetch(name, '2012-01-01', '2012-01-04')
    assert(output.equals(output_should_be))
    timeseries_data.remove_file(name)

def test_parts_to_fetch_left():
    s = mock_fetch('FAKENAME', '2012-01-02', '2012-01-05')
    parts = list(timeseries_data.parts_to_fetch(
        s, pd.to_datetime('2012-01-01'), pd.to_datetime('2012-01-03')))
    assert([(pd.to_datetime(a), pd.to_datetime(b)) for a, b in parts] == [
        (pd.to_datetime('2012-01-01'), pd.to_datetime('2012-01-02')),
        ])

def test_parts_to_fetch_right():
    s = mock_fetch('FAKENAME', '2012-01-02', '2012-01-05')
    parts = list(timeseries_data.parts_to_fetch(
        s, pd.to_datetime('2012-01-08'), pd.to_datetime('2012-01-09')))
    assert([(pd.to_datetime(a), pd.to_datetime(b)) for a, b in parts] == [
        (pd.to_datetime('2012-01-05'), pd.to_datetime('2012-01-09')),
        ])

def test_parts_to_fetch_leftright():
    s = mock_fetch('FAKENAME', '2012-01-02', '2012-01-05')
    parts = list(timeseries_data.parts_to_fetch(
        s, pd.to_datetime('2012-01-01'), pd.to_datetime('2012-01-07')))
    assert([(pd.to_datetime(a), pd.to_datetime(b)) for a, b in parts] == [
        (pd.to_datetime('2012-01-01'), pd.to_datetime('2012-01-02')),
        (pd.to_datetime('2012-01-05'), pd.to_datetime('2012-01-07')),
        ])

def test_parts_to_fetch_leftright2():
    s = mock_fetch('FAKENAME', '2012-01-02', '2012-01-05')
    parts = list(timeseries_data.parts_to_fetch(
        s, None, pd.to_datetime('2012-01-09')))
    assert([(pd.to_datetime(a), pd.to_datetime(b)) for a, b in parts] == [
        (None, pd.to_datetime('2012-01-02')),
        (pd.to_datetime('2012-01-05'), pd.to_datetime('2012-01-09')),
        ])
