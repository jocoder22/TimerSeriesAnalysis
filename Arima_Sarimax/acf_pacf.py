#!/usr/bin/env python
# import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, date
import pandas_datareader as pdr

from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.arima_model import ARMA

sp = '\n\n'

# path = "C:\\Users\\okigboo\\Desktop\\TimeSeriesAnalysis"
# os.chdir(path)

symbol = 'AAPL'
starttime = datetime(2006, 1, 1)
today = date.today()
apple = pdr.get_data_yahoo(symbol, starttime, today)

