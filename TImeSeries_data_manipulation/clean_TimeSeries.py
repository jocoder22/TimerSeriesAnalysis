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
        
