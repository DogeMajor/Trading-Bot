
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../bin')))
import timeseries_data

def test_closure_series_path():
    path = timeseries_data.closure_series_path('abc')
    path_should_be = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../data/price_timeseries', 'abc.csv'))
    assert(path==path_should_be)
