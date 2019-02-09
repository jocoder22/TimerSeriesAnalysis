#!/usr/bin/env python
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader as pdr
from datetime import datetime
from statsmodels.tsa.arima_process import ArmaProcess
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.arima_model import ARMA
from statsmodels.graphics.tsaplots import plot_pacf

# https://www.lfd.uci.edu/~gohlke/pythonlibs/
# http://blog.gregzaal.com/how-to-install-ffmpeg-on-windows/
import talib

stocksname = ['LNG']
stocksname2 = ['SPY']

startdate = datetime(2016, 4, 15)
enddate = datetime(2018, 4, 10)

lng_df = pdr.get_data_yahoo(stocksname, startdate, enddate)[
    ['Adj Close', 'Volume']]

spy_df = pdr.get_data_yahoo(stocksname2, startdate, enddate)[
    ['Adj Close', 'Volume']]
spy_df.columns = ['Adj_Close', 'Volume']
lng_df.columns = ['Adj_Close', 'Volume']






feature_names = ['5d_close_pct']  # a list of the feature names for later

# Create moving averages and rsi for timeperiods of 14, 30, 50, and 200
for n in [14, 30, 50, 200]:

    # Create the moving average indicator and divide by Adj_Close
    lng_df['ma{}'.format(n)] = talib.SMA(lng_df['Adj_Close'].values,
                                      timeperiod=n) / lng_df['Adj_Close']
    # Create the RSI indicator
    lng_df[f'rsi{n}'] = talib.RSI(lng_df['Adj_Close'].values, timeperiod=n) 
    lng_df[f'rm{n}'] = lng_df['Adj_Close'].rolling(n).mean()

    # Create the moving average indicator and divide by Adj_Close
    spy_df['ma{}'.format(n)] = talib.SMA(spy_df['Adj_Close'].values,
                                      timeperiod=n) / lng_df['Adj_Close']
    # Create the RSI indicator
    spy_df[f'rsi{n}'] = talib.RSI(spy_df['Adj_Close'].values, timeperiod=n) 
    spy_df[f'rm{n}'] = spy_df['Adj_Close'].rolling(n).mean()


    # Add rsi. rollingmean and moving average to the feature name list
    feature_names.extend([f'ma{n}', f'rsi{n}', f'rm{n}'])


print(feature_names)

print(lng_df.head())
print(spy_df.head())

print(lng_df.tail())
print(spy_df.tail())
