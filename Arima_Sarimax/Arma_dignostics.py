#!/usr/bin/env python
# import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, date, timedelta
import pandas_datareader as pdr

from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.arima_model import ARMA
from statsmodels.tsa.seasonal import seasonal_decompose

import statsmodels.tsa.api as smt
import statsmodels.api as sm

import warnings
warnings.filterwarnings("ignore")
sp = '\n\n'

symbol = 'AMZN'
starttime = datetime(2006, 1, 1)
today = date.today()
apple = pdr.get_data_yahoo(symbol, starttime, today)

logid = np.log(apple['Close'])
season_x = 24

# Add seasonal decomposition
decomp_seasons = seasonal_decompose(apple.loc['2016':,['Close']], freq=season_x)
decomp_seasons.plot()
plt.show()

# Seasonality check
apple22 = apple['Close'].diff().diff(season_x).dropna()
fig, (ax1, ax2) = plt.subplots(2,1, figsize=(12,8))
plot_acf(apple22, lags=16, zero=False, ax=ax1)
plot_pacf(apple22, lags=16, zero=False, ax=ax2)
plt.title('Show Seasonality')
plt.show()

lags = [season_x*a for a in range(1,6)]

# plot the seasonal lags
fig, (ax1, ax2) = plt.subplots(2,1, figsize=(12,8))
plot_acf(apple22, lags=lags, zero=False, ax=ax1)
plot_pacf(apple22, lags=lags, zero=False, ax=ax2)
plt.title('Show Seasonality2')
plt.show()



# Select year 2016 and beyond only
apple = apple.loc['2016':,['Close']]


# Subtract the rolling mean
apple_2 = apple - apple.rolling(26).mean()

# Drop the NaN values
apple_2 = apple_2.dropna()

# Create figure and subplots
fig, (ax1, ax2) = plt.subplots(2,1, figsize=(12,8))

# Plot the ACF and PACF
plot_acf(apple_2['Close'], lags=75, zero=False, ax=ax1)
plot_pacf(apple_2['Close'], lags=75, zero=False, ax=ax2)

plt.title('Rolling Means')
# Show figure
plt.show()


# using one-step ahead forecast
# model = SARIMAX(apple['Close'], order=(0,1,0), trend='c').fit()
model = SARIMAX(apple.loc['2016':,['Close']], trend='n',
    order=(0, 1, 0),
    seasonal_order=(0, 1, 1, 18),
    enforce_stationarity=True,
    enforce_invertibility=False)

results = model.fit()
residuals = results.resid
print(np.mean(np.abs(residuals)))

# plot the diagnostics
results.plot_diagnostics()
plt.show()

print(results.summary())

