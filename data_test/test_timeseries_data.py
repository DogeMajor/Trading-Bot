
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../bin')))
import timeseries_data

timeseries_data.clear_data()

df = timeseries_data.closure_series('AAPL')
# df = timeseries_data.closure_series('STERV')

assert(df.any())

timeseries_data.clear_data()