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


startdate = datetime(2010, 1, 4)
enddate = datetime(2015, 1, 31)

stocks = ['FB', 'GM', 'KMI', 'YAHOY']
close_price = pdr.get_data_yahoo(stocks, startdate, enddate)['Adj Close']

# Visualize the dataset
close_price.plot(legend=False)
plt.tight_layout()
plt.show()

# Count the missing values of each time series
missing_values = close_price.isna().sum()
print(missing_values)

stocks = ['BAC']
cprice = pdr.get_data_yahoo(stocks, startdate, enddate)['Adj Close']

cprice[24:90] = np.nan
cprice[524:570] = np.nan
cprice[894:956] = np.nan
# linear interpolations
close_price_pol = cprice.interpolate('linear')


# plot the interoplated values
fig, ax = plt.subplots()
close_price_pol.plot(c='g', ax=ax, lw=2)
cprice.plot(c='k', ax=ax)
plt.show()


# Create a function we'll use to interpolate and plot
def interpolate_and_plot(prices, interpolation):

    # Create a boolean mask for missing values
    missing_values = prices.isna()

    # Interpolate the missing values
    prices_interp = prices.interpolate(interpolation)

    # Plot the results, highlighting the interpolated values in black
    fig, ax = plt.subplots(figsize=(10, 5))
    prices_interp.plot(color='k', alpha=.6, ax=ax, legend=False)

    # Now plot the interpolated values on top in red
    prices_interp[missing_values].plot(ax=ax, color='r', lw=3, legend=False)
    ax.set(title=f"Interpolation using {interpolation} function")
    plt.show()


# using latest non-missing values
interpolation_type = 'zero'
interpolate_and_plot(cprice, interpolation_type)

# linear interpolation
interpolation_type = 'linear'
interpolate_and_plot(cprice, interpolation_type)

# using quadratic function
interpolation_type = 'quadratic'
interpolate_and_plot(cprice, interpolation_type)
