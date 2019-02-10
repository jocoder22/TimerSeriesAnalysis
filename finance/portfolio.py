import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import datasets
plt.style.use('ggplot')
import pandas_datareader as pdr
from datetime import datetime

startdate = datetime(2010,1,4)
enddate = datetime(2019,1,31)

stocklist = ['AAPL', 'ABT', 'AIG','AMAT', 'ARNC', 'BAC', 'BSX', 'C',  'CMCSA',
             'CSCO', 'DAL', 'EBAY', 'F', 'FB', 'FCX', 'FITB', 'FOXA', 'FTR', 'GE',
             'GILD', 'GLW', 'GM', 'HAL', 'HBAN', 'JPM', 'KEY', 'HPQ', 'INTC',
             'KMI', 'KO', 'MRK', 'MRO', 'MSFT', 'MU', 'NFLX', 'NVDA', 'ORCL', 'PFE',
             'QCOM', 'RF', 'SBUX', 'T', 'V', 'VZ', 'WFC', 'XOM', 'XRX', 'YAHOY']

allstocks = pdr.get_data_yahoo(stocklist, startdate, enddate)['Adj Close']

# Resample the full dataframe to monthly timeframe
monthly_sample = allstocks.resample('BMS').first()

# Calculate daily returns of stocks
returns_daily = allstocks.pct_change()

# Calculate monthly returns of the stocks
returns_monthly = monthly_sample.pct_change().dropna()
print(returns_monthly.tail())

print(allstocks.head())