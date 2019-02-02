#!/usr/bin/env python
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import datetime
import pandas_datareader as pdr
from math import sqrt

# https: // fred.stlouisfed.org/search?st = interest+rate
path = "C:\\Users\\okigboo\\Desktop\\TimeSeriesAnalysis"
os.chdir(path)

symbol = 'AAPL'
starttime = datetime.datetime(2000, 1, 1)
endtime = datetime.datetime(2019, 1, 31)
apple = pdr.get_data_yahoo(symbol, starttime, endtime)


symbol = "^GSPC"
sp500 = pdr.get_data_yahoo(symbol, starttime, endtime)


sp500A = sp500[['Adj Close']].rename(index=str, columns={'Adj Close': 'SP500'})
appleA = apple[['Adj Close']].rename(index=str, columns={'Adj Close': 'Apple'})



alldata = sp500A.join(appleA, how='inner')
df = alldata.pct_change()
correlation = df['SP500'].corr(df['Apple'])
print(f'The correlation between sp500 and Apple stock is {correlation}')

df = sm.add_constant(df)
df = df.dropna()


results = sm.OLS(df['SP500'], df[['const','Apple']]).fit()
print(results.summary())

print(dir(results))


print('Parameters: ', results.params)
print('R2: ', results.rsquared)

correlation2 = sqrt(results.rsquared)
print(correlation, correlation2)



# Authocorrelation
symbol = 'MSFT'
MSFT = pdr.get_data_yahoo(symbol, starttime, endtime)

MSFT = MSFT.resample(rule='W').last()

# Compute the percentage change of prices
returns = MSFT.pct_change()

# Compute and print the autocorrelation of returns
autocorrelation = returns['Adj Close'].autocorr()
print("The autocorrelation of weekly returns is %4.2f" % (autocorrelation))


################### From Fred: contains daily data of 10-year interest
# https: // fred.stlouisfed.org/
starttime = datetime.datetime(1962, 1, 1)
endtime = datetime.datetime(2019, 1, 31)
daily_data = pdr.DataReader('DGS10', 'fred', starttime, endtime)

# Compute the daily change in interest rates
daily_data['change_rates'] = daily_data.diff()

# Compute and print the autocorrelation of daily changes
autocorrelation_daily = daily_data['change_rates'].autocorr()
print("The autocorrelation of daily interest rate changes is %4.2f" %
      (autocorrelation_daily))

# Convert the daily data to annual data
annual_data = daily_data['DGS10'].resample(rule='A').last()

# Repeat above for annual data
annual_data['diff_rates'] = annual_data.pct_change()
autocorrelation_annual = annual_data['diff_rates'].autocorr()
print("The autocorrelation of annual interest rate changes is %4.2f" %
      (autocorrelation_annual))

