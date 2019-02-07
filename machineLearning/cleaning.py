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

# linear interpolations
close_price_pol = close_price.interpolate('linear')


# plot the interoplated values
fig, ax = plt.subplots()
ax = close_price_pol.plot(c='g')
close_price.plot(c='k', ax=ax, lw=3)
plt.show()



