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

apple['Close'].plot()
plt.show()
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



# using dynamic predictions
model_dynamic = SARIMAX(apple['Close'], order=(0,1,0), trend='c').fit()

# make in-sample prediction
prediction_dynamic = model_dynamic.get_prediction(start=-125, dynamic=True)

# Extract prediction mean
mean_prediction_dynamic = prediction_dynamic.predicted_mean

# Get confidence intervals of  predictions
confidence_intervals_dynamic = prediction_dynamic.conf_int()

# Select lower and upper confidence limits
lower_limits_dynamic = confidence_intervals_dynamic.loc[:,'lower Close']
upper_limits_dynamic = confidence_intervals_dynamic.loc[:,'upper Close']


# plot the apple data
plt.plot(apple.index, apple['Close'], label='observed')

# plot your mean prediction
plt.plot(mean_prediction_dynamic.index, mean_prediction_dynamic, color='r', label='prediction')

# shade the area between your confidence limits
plt.fill_between(mean_prediction_dynamic.index, lower_limits_dynamic, 
         upper_limits_dynamic, color='pink')

# set labels, legends and show plot
plt.xlabel('Date')
plt.ylabel('apple Stock Price - Close USD')
plt.legend()
plt.show()




# using one-step ahead forecast
# model = SARIMAX(apple['Close'], order=(0,1,0), trend='c').fit()
mymodel = SARIMAX(apple['Close'],
    order=(0, 1, 0),
    seasonal_order=(0, 1, 0, 7),
    enforce_stationarity=True,
    enforce_invertibility=False)

N = 250
next_day = apple.index[-1] + timedelta(days=1)
forecast_index = pd.date_range(start=next_day, freq='B', periods=N)

model = mymodel.fit()
# make forecast
# forecast = model.get_forecast(steps=N)
forecast = model.forecast(steps=N)


# form dataframe with the new dates
result = pd.DataFrame(list(zip(list(forecast_index),list(forecast))),
        columns=['Date','ForecastPrice']).set_index('Date')


# plot the apple data
plt.plot(apple.index, apple['Close'], label='observed')

# plot your mean prediction
plt.plot(result.index, result['ForecastPrice'], color='r', label='Forecast')

# # shade the area between your confidence limits
# plt.fill_between(result.index, lower_limits_forecast, 
#          upper_limits_forecast, color='pink')

# set labels, legends and show plot
plt.xlabel('Date')
plt.ylabel('apple Stock Price - Close USD')
plt.legend()
plt.show()







# Making forecast
prediction2 = model.get_forecast(steps=N)

# Extract forecast mean
mean_forecast = prediction2.predicted_mean

# form dataframe with the new dates
forecast_df = pd.DataFrame(list(zip(list(forecast_index),list(mean_forecast))),
        columns=['Date','ForecastPrice'])


print(forecast_df, sep=sp)
# Get confidence intervals of  forecast and remove the index
confidence_intervals_forecast = prediction2.conf_int().reset_index(drop=True)
confidence_intervals_forecast['mp'] = confidence_intervals_forecast.mean(axis=1)
print(confidence_intervals_forecast.head(), end=sp)

# print(confidence_intervals_forecast)
# # concatenate the forecast confidence intervals
result = pd.concat([forecast_df, confidence_intervals_forecast], axis=1).set_index('Date')

# result['mp'] = result.loc[:,['lower Close', 'upper Close']].mean(axis=1)
print(result.head(), result.index, sep=sp, end=sp)

# # Select lower and upper confidence limits
lower_limits_forecast = result.loc[:,'lower Close']
upper_limits_forecast = result.loc[:,'upper Close']




# print(result.head())

# plot the apple data
plt.plot(apple.index, apple['Close'], label='observed')

# plot your mean prediction
plt.plot(result.index, result['ForecastPrice'], color='r', label='Forecast')

# shade the area between your confidence limits
plt.fill_between(result.index, lower_limits_forecast, 
         upper_limits_forecast, color='pink')

# set labels, legends and show plot
plt.xlabel('Date')
plt.ylabel('apple Stock Price - Close USD')
plt.legend()
plt.show()


