#!/usr/bin/env python
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import datetime
import pandas_datareader as pdr


# https: // fred.stlouisfed.org/search?st = interest+rate
# https://www.quantopian.com/posts/enhancing-short-term-mean-reversion-strategies-1

path = "C:\\Users\\okigboo\\Desktop\\TimeSeriesAnalysis"
# path = 'C:\\Users\\Jose\\Desktop\\TimerSeriesAnalysis'
os.chdir(path)

symbol = 'AAPL'
starttime = datetime.datetime(2000, 1, 1)
endtime = datetime.datetime(2019, 1, 31)
apple = pdr.get_data_yahoo(symbol, starttime, endtime)


print(apple.head())
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

correlation2 = np.sqrt(results.rsquared)
print(correlation, correlation2)


