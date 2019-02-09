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

stocksname = ['LNG', 'SPY']

startdate = datetime(2016, 4, 15)
enddate = datetime(2018, 4, 10)

stock = pdr.get_data_yahoo(stocksname, startdate, enddate)[
    ['Adj Close', 'Volume']]
lng_df = stock.loc[:, (slice(None), 'LNG')]
spy_df = stock.loc[:, (slice(None), 'SPY')]

spy_df.columns = spy_df.columns.get_level_values(0)
lng_df.columns = lng_df.columns.get_level_values('Attributes')
