#!/usr/bin/env python
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader as pdr
from datetime import datetime
from statsmodels.tsa.arima_process import ArmaProcess
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.arima_model import ARMA
from statsmodels.graphics.tsaplots import plot_pacf

from sklearn.linear_model import Ridge
from sklearn.model_selection import cross_val_score

startdate = datetime(2010,1,4)
enddate = datetime(2015,1,31)

stocks = ['EBAY', 'YAHOY']
data = pdr.get_data_yahoo(stocks, startdate, enddate)['Adj Close']

# Visualize the dataset
data.plot(legend=False)
plt.tight_layout()
plt.show()

# Count the missing values of each time series
missing_values = data.isna().sum()
print(missing_values)

# Scatterplot stocks prices
data.plot.scatter('EBAY', 'YAHOY')
plt.show()


# Scatterplot with color relating to time
data.plot.scatter('EBAY', 'YAHOY', c=data.index,
                    cmap=plt.cm.viridis, colorbar=False)
plt.show()
# stocklist = ['HPE']

stocklist = ['AAPL', 'ABT', 'AIG','AMAT', 'ARNC', 'BAC', 'BSX', 'C',  'CMCSA',
             'CSCO', 'DAL', 'EBAY', 'F', 'FB', 'FCX', 'FITB', 'FOXA', 'FTR', 'GE',
             'GILD', 'GLW', 'GM', 'HAL', 'HBAN', 'JPM', 'KEY', 'HPQ', 'INTC',
             'KMI', 'KO', 'MRK', 'MRO', 'MSFT', 'MU', 'NFLX', 'NVDA', 'ORCL', 'PFE',
             'QCOM', 'RF', 'SBUX', 'T', 'V', 'VZ', 'WFC', 'XOM', 'XRX', 'YAHOY']

allstocks = pdr.get_data_yahoo(stocklist, startdate, enddate)['Adj Close']
missing_values = allstocks.isna().sum()
pp = missing_values.index[missing_values.values > 0]
print(missing_values)

missingstocks = allstocks[list(pp)]
missingstocks.plot()
plt.show()


allstocks.fillna(method='bfill', inplace=True)
print(allstocks.head())

NON_LABELS = [c for c in allstocks.columns if c != 'AAPL']
print(NON_LABELS)

X = allstocks.drop('AAPL', axis=1)
y = allstocks['AAPL']

scores = cross_val_score(Ridge(), X, y, cv=6)
print(scores)



# Split our data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                    train_size=.8, shuffle=False, random_state=1)

# Fit our model and generate predictions
model = Ridge()
model.fit(X_train, y_train)
predictions = model.predict(X_test)
score = r2_score(y_test, predictions)
print(score)


# Visualize our predictions along with the "true" values, and print the score
# convert prediction, np arrays to pandas Series
predictions_series = pd.Series(predictions, index=y_test.index)
plt.subplot(1,1,1)
y_test.plot(color='k', lw=3, label="Actual Prices")
predictions_series.plot(color='r', lw=2, label="Predicted Prices")
plt.title("Actual and Predicted Prices")
plt.legend()
plt.show()

# fig, ax = plt.subplots()
# ax.plot(y_test, color='k', lw=3, label="Actual Prices")
# ax.plot(predictions_series, color='r', lw=2, label="Predicted Prices")
# ax.set(title=" Actual and Predicted Prices")
# plt.legend()
# plt.show()
