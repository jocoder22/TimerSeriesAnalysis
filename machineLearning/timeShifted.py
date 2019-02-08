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

stock = pdr.get_data_yahoo('APPL', startdate, enddate)['Adj Close']

print(stock.head())
