#!/usr/bin/env python
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader as pdr
import yfinance as yf
from datetime import datetime
from statsmodels.tsa.arima_process import ArmaProcess
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.arima_model import ARMA
from statsmodels.graphics.tsaplots import plot_pacf

yf.pdr_override() # good for single data download only

stocksname = 'LNG SPY'
startdate = datetime(2016, 4, 15)
enddate = datetime(2018, 4, 10)

stock = yf.download(stocksname, startdate, enddate)[['Adj Close', 'Volume']]
lng_df = stock.loc[:, (slice(None), 'LNG')]
spy_df = stock.loc[:, (slice(None), 'SPY')]

lng2 = lng_df.droplevel(1, axis=1)
spy2 = spy_df.droplevel(1, axis=1)

spy_df.columns = spy_df.columns.get_level_values(0)
lng_df.columns = lng_df.columns.get_level_values(0)

print(stock.head())
print(lng_df.head())  
print(spy_df.head())
print(lng_df.columns)

# Plot the Adj Close columns for SPY and LNG
spy_df['Adj Close'].plot(label='SPY', legend=True)
lng_df['Adj Close'].plot(label='LNG', legend=True, secondary_y=True, mark_right=False)
plt.tick_params(axis='y', colors=plt.gca().lines[-1].get_color())
plt.show()  # show the plot
plt.clf()  # clear the plot space

# Histogram of the daily price change percent of Adj Close for LNG
lng_df['Adj Close'].pct_change().plot.hist(bins=50)
plt.xlabel('adjusted close 1-day percent change')
plt.show()


# Create 5-day % changes of Adj Close for the current day, and 5 days in the future
lng_df['5d_future_close'] = lng_df['Adj Close'].shift(-5)
lng_df['5d_close_future_pct'] = lng_df['5d_future_close'].pct_change(5)
lng_df['5d_close_pct'] = lng_df['Adj Close'].pct_change(5)

# Calculate the correlation matrix between the 5d close pecentage changes (current and future)
corr = lng_df[['5d_close_pct', '5d_close_future_pct']].corr()
print(corr)


# Scatter the current 5-day percent change vs the future 5-day percent change
plt.scatter(lng_df['5d_close_pct'], lng_df['5d_close_future_pct'])
plt.show()
