#!/usr/bin/env python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import pandas_datareader as pdr
from datetime import datetime
from statsmodels.tsa.stattools import kpss, adfuller

#########################################################################################################
####################################
####################################  Kwiatkowski-Phillips-Schmidt-Shin (KPSS) test 
####################################
#########################################################################################################

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
      
# regression str{“c”, “ct”}
# The null hypothesis for the KPSS test.

# “c” : The data is stationary around a constant (default).

# “ct” : The data is stationary around a trend i.e around a deterministic trend. 
      
statistic, p_value, n_lags, critical_values = kpss(allstocks, nlags="auto", regression="ct")
print(f'KPSS Result: The series is {"not " if p_value < 0.05 else ""}stationary')      
      
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
      
# KPSS on log returns     
logret = allstocks.pct_change().dropna()
print(logret.head())
_, p_value, _, _ = kpss(logret, nlags="auto")
print(f'KPSS Result: The series is {"not" if p_value < 0.05 else ""} stationary')   
      
#########################################################################################################
####################################
####################################  the Augmented Dickey Fuller (ADF) test 
####################################
#########################################################################################################
      
# The null hypothesis of the Augmented Dickey-Fuller is that there is a unit root, with the alternative that there is no unit root. 
# If the pvalue is above a critical size, then we cannot reject that there is a unit root. 
# the null hypothesis in ADF test is the series is not stationary.
      
###  Returns
# adffloat - The test statistic.
# pvaluefloat - MacKinnon”s approximate p-value based on MacKinnon (1994, 2010).
# usedlagint - The number of lags used.
# nobsint - The number of observations used for the ADF regression and calculation of the critical values.
# critical valuesdict - Critical values for the test statistic at the 1 %, 5 %, and 10 % levels. Based on MacKinnon (2010).
# icbestfloat - The maximized information criterion if autolag is not None.
# resstoreResultStore, optional - A dummy class with results attached as attributes. 
      
# ADF on raw data     
result = adfuller(allstocks, autolag='AIC')
print(f'ADF Result: The series is {"not" if result[1] > 0.05 else ""} stationary') 
      
# ADF on first differenced data
result = adfuller(diffstocks, autolag='AIC')
print(f'ADF Result: The series is {"not" if result[1] > 0.05 else ""} stationary') 
 
# ADF on returns  
result = adfuller(ret, autolag='AIC')
print(f'ADF Result: The series is {"not " if result[1] > 0.05 else ""}stationary')
      
# ADF on log returns        
result = adfuller(logret, autolag='AIC')
print(f'ADF Result: The series is {"not " if result[1] > 0.05 else ""}stationary')
      
      
# https://otexts.com/fpp2/stationarity.html
<<<<<<< HEAD
    
# https://www.machinelearningplus.com/time-series/vector-autoregression-examples-python/
ML+ML+
#Vector Autoregression (VAR) - Comprehensive Guide with Examples in Python - ML+
=======
>>>>>>> a27ad802d4ba2fbdccd9f8648a8153e2f6d5e150
