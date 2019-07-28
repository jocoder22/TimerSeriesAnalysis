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

import statsmodels.tsa.api as smt
import statsmodels.api as sm

import warnings
warnings.filterwarnings("ignore")

sp = '\n\n'

symbol = 'AAPL'
starttime = datetime(2006, 1, 1)
today = date.today()
apple = pdr.get_data_yahoo(symbol, starttime, today)

# one lag differencing to make our data stationary
apple['Close1d'] = apple['Close'].diff()
apple.dropna(inplace=True)

print(apple.head(), len(apple), sep=sp)


# using one-step predictions
model = SARIMAX(apple['Close'], order=(0,1,0), trend='c').fit()
# results = model.fit()
# make in-sample prediction
prediction = model.get_prediction(start=-225)

# Extract prediction mean
mean_prediction = prediction.predicted_mean

# Get confidence intervals of  predictions
confidence_intervals = prediction.conf_int()

# Select lower and upper confidence limits
lower_limits = confidence_intervals.loc[:,'lower Close']
upper_limits = confidence_intervals.loc[:,'upper Close']

# Print best estimate  predictions
print(mean_prediction[:5])


# plot the apple data
plt.plot(apple.index, apple['Close'], label='observed', color='black')

# plot your mean prediction
plt.plot(mean_prediction.index, mean_prediction, color='y', label='prediction')

# shade the area between your confidence limits
plt.fill_between(mean_prediction.index, lower_limits, 
         upper_limits, color='pink')

# set labels, legends and show plot
plt.xlabel('Date')
plt.ylabel('apple Stock Price - Close USD')
plt.legend()
plt.show()

