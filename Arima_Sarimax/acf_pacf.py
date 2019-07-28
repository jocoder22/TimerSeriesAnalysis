#!/usr/bin/env python
# import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, date
import pandas_datareader as pdr

from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.arima_model import ARMA

sp = '\n\n'

# path = "C:\\Users\\okigboo\\Desktop\\TimeSeriesAnalysis"
# os.chdir(path)

symbol = 'AAPL'
starttime = datetime(2006, 1, 1)
today = date.today()
apple = pdr.get_data_yahoo(symbol, starttime, today)


print(apple.head())

# There is upward trend in the apple close as show by the plot
fig, (ax1, ax2) = plt.subplots(2,1, figsize=(12,8))
apple.Close.plot(ax=ax1)
apple.Volume.plot(ax=ax2)
plt.show()

# let's perform statistical test: adfuller test
### this shows that there is trend 
result = adfuller(apple['Close'])
print(f'Test Statistic: {result[0]}\nP-value: {result[1]}\nCritical Values: {result[4]}')


# do one lag differencing
result = adfuller(apple['Close'].diff().dropna())
print(f'Test Statistic: {result[0]}\nP-value: {result[1]}\nCritical Values: {result[4]}')

# plot the one lag differencing
apple['Close'].diff().dropna().plot()
plt.show()

# plot the acf and pacf
apple['Close1d'] = apple['Close'].diff()
apple.dropna(inplace=True)
print(apple.head())
fig, (ax1, ax2) = plt.subplots(2,1, figsize=(12,8))
plot_acf(apple['Close1d'], lags=10, zero=False, ax=ax1)
plot_pacf(apple['Close1d'], lags=10, zero=False, ax=ax2)

plt.show()

