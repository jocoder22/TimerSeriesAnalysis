import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import datetime
import pandas_datareader as pdr

path = 'C:\\Users\\Jose\\Desktop\\TimerSeriesAnalysis'
os.chdir(path)

starttime = datetime.datetime(2000, 1, 1)
endtime = datetime.datetime(2019, 1, 31)

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
annual_data['diff_rates'] = annual_data.diff()
autocorrelation_annual = annual_data['diff_rates'].autocorr()
print("The autocorrelation of annual interest rate changes is %4.2f" %
      (autocorrelation_annual))

