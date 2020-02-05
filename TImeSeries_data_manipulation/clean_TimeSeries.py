#!/usr/bin/env python
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import pandas_datareader as pdr
import seaborn as sns
import pandas_datareader.data as wb
from matplotlib.dates import date2num as matdate
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

path = 'D:\TimerSeriesAnalysis\TimeSeries_data_manipulation'
os.chdir(path)

ticker = ['RIO', 'ILMN', 'CPRT', 'EL', 'AMZN', 'PAA', 'GS', 'AMGN', 'MA', 'TEF', 'AAPL', 'UPS']

tickers = ["GOOG", "AAPL", "AMZN"]
names = ["google", "apple", "amazon"]



for idx, elem in enumerate(tickers):
    starttime = datetime.datetime(1999, 1, int(2^idx * 8))
    endtime = datetime.datetime(2019, 1, 31)
    if idx == 0:
        google = pd.DataFrame(pdr.get_data_yahoo(elem, starttime, endtime)['Adj Close'])
    elif idx == 1:
        apple = pd.DataFrame(pdr.get_data_yahoo(elem, starttime, endtime)['Adj Close'])
    else:
        amazon = pd.DataFrame(pdr.get_data_yahoo(elem, starttime, endtime)['Adj Close'])
        

        
indexes = dates = pd.date_range('2000-01-01', '2016-12-31')
all_stocks = pd.DataFrame(index = indexes)

# google = pd.DataFrame(google)

for idx, data in enumerate([google, apple, amazon]):
    data.rename(columns = {"Adj Close": names[idx]}, inplace=True)
    
# all_stocks = pd.concat([google, apple, amazon, all_stocks], axis=1)
# all_stocks = pd.concat([google, apple, amazon, all_stocks], axis=1, join="inner")
all_stocks = pd.concat([google, apple, amazon, all_stocks], axis=1).reindex(all_stocks.index) 
print(google.head(), apple.head, amazon.head(), all_stocks, sep="\n\n")


all_stocks.dropna(axis=0, inplace=True)

print(all_stocks.count(), all_stocks.head(), sep="\n\n")


all_stocks.mean()

# Print the median stock price for each stock
all_stocks.median()
# Print the standard deviation of the stock price for each stock  
all_stocks.std()
# Print the correlation between stocks
all_stocks.corr()
