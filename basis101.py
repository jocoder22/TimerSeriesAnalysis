#!/usr/bin/env python
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import pandas_datareader as pdr

path = "C:\\Users\\okigboo\\Desktop\\TimeSeriesAnalysis"
os.chdir(path)

symbol = 'AAPL'
starttime = datetime.datetime(1990, 1, 1)
endtime = datetime.datetime(2019, 1, 31)
apple = pdr.get_data_yahoo(symbol, starttime, endtime)

symbol = "^GSPC"
sp500 = pdr.get_data_yahoo(symbol, starttime, endtime)

symbol = '^DJI'
dowJones = pdr.get_data_yahoo(symbol, starttime, endtime)

symbol = '^TNX'
usBond = pdr.get_data_yahoo(symbol, starttime, endtime)

print(apple.head())
print(dowJones.head())
print(usBond.head())


amazon = pd.read_csv('AMZN.csv', parse_dates=True, index_col='Date')
print(amazon.head())
print(len(amazon))


# US Bond 29 years closure times
downIndex = set(dowJones.index)
bondIndex = set(usBond.index)
alldiff = downIndex - bondIndex


# US Bond 19 years closure times
downIndex2000 = set(dowJones["2000":].index)
bondIndex2000 = set(usBond["2000":].index)
dff2000 = downIndex2000 - bondIndex2000

# US Bonds closure difference
print(len(alldiff) - len(dff2000))


# US Bond 29 years closure times
sp500Index = set(sp500.index)
bondIndex = set(usBond.index)
alldiffsp = downIndex - bondIndex


# US Bond 19 years closure times
sp500Index2000 = set(sp500["2000":].index)
bondIndex2000 = set(usBond["2000":].index)
dff2000sp = sp500Index2000 - bondIndex2000

# US Bonds closure difference
print(len(alldiffsp) - len(dff2000sp))


# Plot 2012 data using slicing
LABELS = [c for c in amazon.columns if c != 'Volume']
amazon.loc['2012', LABELS].plot()
plt.show()

# Plot the entire time series amazons and show gridlines
amazon[LABELS].plot()
plt.show()

# # This formats the plots such that they appear on separate rows
# fig, axes = plt.subplots(nrows=2, ncols=1)

# # Plot the PDF
# df.fraction.plot(ax=axes[0], kind='hist', bins=30, normed=True, range=(0, .3))
# plt.show()

# # Plot the CDF
# df.fraction.plot(ax=axes[1], kind='hist', bins=30,
#                  normed=True, cumulative=True, range=(0, .3))
# plt.show()


""" 
df.index = pd.to_datetime(df.index)
df['2012']
df1.join(df2)
df = df.resample(rule='W', how='last')
df['col'].pct_change()
df['col'].diff()
df['col1'].corr(df['col2'])
df['col3'].autocorr()

"""
