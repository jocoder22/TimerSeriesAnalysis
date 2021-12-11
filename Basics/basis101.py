#!/usr/bin/env python
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import pandas_datareader as pdr

# path = "C:\\Users\\okigboo\\Desktop\\TimeSeriesAnalysis"
path = r"D:\TimerSeriesAnalysis"
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

# This formats the plots such that they appear on separate rows
# fig, axes = plt.subplots(nrows=2, ncols=1)
plt.subplot(211)
# Plot the PDF
usBond['Open'].plot(kind='hist',
                    bins=30, density=True, edgecolor='black', linewidth=1.2)
# plt.show()

# Plot the CDF
plt.subplot(212)
usBond['Open'].plot(kind='hist', bins=30, density=True, cumulative=True)
plt.show()

sp500A = sp500[['Adj Close']].rename(index=str, columns={'Adj Close': 'SP500'})
print(sp500A.head())
usBondA = usBond[['Adj Close']]
usBondA.rename(index=str, columns={'Adj Close': 'Bond10Y'}, inplace=True)
# usBondA.rename({'Adj Close': 'Bond10Y'}, axis='columns', inplace=True)
print(usBondA.head())

allclose = sp500A.join(usBondA, how='inner')

print(allclose.head())

returns = allclose.pct_change()
correlation = returns['SP500'].corr(returns['Bond10Y'])
print(f'Correlation of sp500 and UsBond10Y is {correlation}')

plt.scatter(returns['SP500'], returns['Bond10Y'])
plt.show()


# https://d2l.ai/chapter_linear-networks/linear-regression.html
# https://eli.thegreenplace.net/2014/derivation-of-the-normal-equation-for-linear-regression/



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

# https://keras.io/guides/transfer_learning/#the-typical-transferlearning-workflow
# https://gogul.dev/software/flower-recognition-deep-learning#keras-pre-trained-models
# https://github.com/fmfn/BayesianOptimization
# https://github.com/borisbanushev/stockpredictionai
