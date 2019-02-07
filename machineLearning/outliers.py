#!/usr/bin/env python
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

stocks = ['EBAY', 'AAPL', 'YAHOY']

startdate = datetime(2010, 1, 4)
enddate = datetime(2015, 1, 31)

porfolio = pdr.get_data_yahoo(stocks, startdate, enddate)['Adj Close']

# porfolio.plot()
# plt.show()


def percent_change(series):
    # Collect all *but* the last value of this window, then the final value
    previous_values = series[:-1]
    last_value = series[-1]

    # Calculate the % difference between the last value and the mean of earlier values
    percent_change = (last_value - np.mean(previous_values)) / np.mean(previous_values)
    
    return percent_change


# # Apply your custom function and plot
prices_perc = porfolio.rolling(920).apply(percent_change)
prices_perc.loc["2014":"2015"].plot()
plt.show()

amean = porfolio['AAPL'].mean()
astd = porfolio['AAPL'].std()
print(amean, astd)

def replace_outliers(series):
    # Calculate the absolute difference of each timepoint from the series mean
    absolute_differences_from_mean = np.abs(series - np.mean(series))

    # Calculate a mask for the differences that are > 3 standard deviations from zero
    this_mask = absolute_differences_from_mean > (np.std(series) * 3)

    # Replace these values with the median accross the data
    series[this_mask] = np.nanmedian(series)
    return series


# # Apply your preprocessing function to the timeseries and plot the results
prices_perc_replace = prices_perc.apply(replace_outliers)
prices_perc_replace.loc["2014":"2015"].plot()
plt.show()

fig, ax = plt.subplots()
prices_perc.loc["2014":"2015", 'AAPL'].plot(ax=ax, c='red')
prices_perc_replace.loc["2014":"2015", 'AAPL'].plot(ax=ax, c='g')
plt.show()
