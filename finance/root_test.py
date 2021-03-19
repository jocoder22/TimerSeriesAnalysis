#!/usr/bin/env python
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import pandas_datareader as pdr
from datetime import datetime
from statsmodels.tsa.stattools import kpss

# Kwiatkowski-Phillips-Schmidt-Shin (KPSS) test (Kwiatkowski, Phillips, Schmidt, & Shin, 1992). 
# In this test, the null hypothesis is that the data are stationary, 
# and we look for evidence that the null hypothesis is false.

# Kwiatkowski, D., Phillips, P. C. B., Schmidt, P., & Shin, Y. (1992). 
# Testing the null hypothesis of stationarity against the alternative of a unit root: How sure are we that economic time series have a unit root? 
# Journal of Econometrics, 54(1-3), 159–178. https://doi.org/10.1016/0304-4076(92)90104-Y

# A key difference from ADF test is the null hypothesis of the KPSS test is that the series is stationary.
# So practically, the interpretaion of p-value is just the opposite to each other.

# The test statistic should be smaller

startdate = datetime(2013, 2, 2)


stocklist = ['AAPL', 'ABT', 'AIG','AMAT', 'ARNC', 'BAC', 'BSX', 'C',  'CMCSA',
             'CSCO', 'DAL', 'EBAY', 'F', 'FB', 'FCX', 'FITB', 'FOXA', 'FTR', 'GE',
             'GILD', 'GLW', 'GM', 'HAL', 'HBAN', 'JPM', 'KEY', 'HPQ', 'INTC',
             'KMI', 'KO', 'MRK', 'MRO', 'MSFT', 'MU', 'NFLX', 'NVDA', 'ORCL', 'PFE',
             'QCOM', 'RF', 'SBUX', 'T', 'V', 'VZ', 'WFC', 'XOM', 'XRX', 'YAHOY']

allstocks = pdr.get_data_yahoo(stocklist, startdate, enddate)['Adj Close']
print(allstocks.head())
statistic, p_value, n_lags, critical_values = kpss(series, **kw)
print(f'KPSS Result: The series is {"not " if p_value < 0.05 else ""}stationary')
