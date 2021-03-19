#!/usr/bin/env python
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
stock = ['AAPL']

allstocks = pdr.get_data_yahoo(stock, startdate)['Adj Close']
print(allstocks.head())

# KPSS on raw data
statistic, p_value, n_lags, critical_values = kpss(allstocks, nlags="auto")
print(f'KPSS Result: The series is {"not" if p_value < 0.05 else ""} stationary')
      
      
# KPSS on first differenced data
diffstocks = allstocks.diff().dropna()
print(diffstocks.head())
statistic, p_value, n_lags, critical_values = kpss(diffstocks, nlags="auto")
print(f'KPSS Result: The series is {"not" if p_value < 0.05 else ""} stationary')
 
# KPSS on returns     
ret = allstocks.pct_change().dropna()
print(ret.head())
_, p_value, _, _ = kpss(ret, nlags="auto")
print(f'KPSS Result: The series is {"not" if p_value < 0.05 else ""} stationary')          
      
      
