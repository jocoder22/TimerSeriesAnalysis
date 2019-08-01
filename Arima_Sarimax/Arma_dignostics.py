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

symbol = 'AMZN'
starttime = datetime(2006, 1, 1)
today = date.today()
apple = pdr.get_data_yahoo(symbol, starttime, today)


# using one-step ahead forecast
# model = SARIMAX(apple['Close'], order=(0,1,0), trend='c').fit()
mymodel = SARIMAX(apple['Close'],
    order=(0, 1, 0),
    seasonal_order=(0, 1, 0, 90),
    enforce_stationarity=True,
    enforce_invertibility=False)

