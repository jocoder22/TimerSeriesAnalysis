#!/usr/bin/env python
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import pandas_datareader as pdr

path = "C:\\Users\\okigboo\\Desktop\\TimeSeriesAnalysis"
os.chdir(path)

symbol = 'AAPL'
starttime = datetime.datetime(2010, 1, 1)
endtime = datetime.datetime(2019, 1, 31)
apple = pdr.get_data_yahoo(symbol, starttime, endtime)


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

# # This formats the plots such that they appear on separate rows
# fig, axes = plt.subplots(nrows=2, ncols=1)

# # Plot the PDF
# df.fraction.plot(ax=axes[0], kind='hist', bins=30, normed=True, range=(0, .3))
# plt.show()

# # Plot the CDF
# df.fraction.plot(ax=axes[1], kind='hist', bins=30,
#                  normed=True, cumulative=True, range=(0, .3))
# plt.show()
