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

import warnings
warnings.filterwarnings('ignore')

sp = '\n\n'

symbol = 'AAPL'
starttime = datetime(2006, 1, 1)
today = date.today()
apple = pdr.get_data_yahoo(symbol, starttime, today)

print(apple.head())
# do grid search for parameters
gridlist = []

# Loop over p values from 0-3
for p in range(4):

    # Loop over q values from 0-3
    for q in range(4):

        # Loop over for the trend values
        for t in ['n','c','t','ct']:

            try:
                # create and fit SARIMA(p,1,q) model
                model = SARIMAX(apple.loc['2016':,['Close']], order=(p,1,q), trend=t)
                results = model.fit()
                
                # Calculate the mean absolute error from residuals
                mae0 = np.mean(np.abs(results.resid))

                # Print order and results
                gridlist.append((p,q, results.aic, results.bic, mae0, t))
                
            except:
                gridlist.append((p,q, None, None, None, None))

# Construct DataFrame from gridlist
griddataframe = pd.DataFrame(gridlist, 
                        columns=['p', 'q', 'AIC', 'BIC', 'MAE', 'T'])

print(griddataframe, end=sp)


# Print griddataframe in order of increasing AIC
print('Based on AIC:', griddataframe.sort_values('AIC').head(1), end=sp, sep='\n')

# Print griddataframe in order of increasing BIC
print('Based on BIC:\n', griddataframe.sort_values('BIC').head(1), end=sp)

# Print griddataframe in order of increasing MAE
print('Based on MAE:\n', griddataframe.sort_values('MAE').head(1), end=sp)

'''
# do grid search for parameters
gridlist2 = []

# Loop over p values from 0-3
for P in range(4):

    # Loop over q values from 0-3
    for Q in range(4):

        for D in range(3):

            # Loop over for the trend values
            for tr in ['n', 't']:

                for M in [7, 30, 60, 90]:

                    try:
                        # create and fit SARIMA model
                        model = SARIMAX(apple['Close'], order=(0, 1, 0), trend=tr,
                            seasonal_order=(P, D, Q, M), 
                            enforce_stationarity=False, 
                            enforce_invertibility=False)

                        results = model.fit()
                        
                        # Calculate the mean absolute error from residuals
                        mae0 = np.mean(np.abs(results.resid))

                        # Print order and results
                        gridlist2.append((P, D, Q, M, results.aic, results.bic, mae0, tr))
                        
                    except:
                        gridlist2.append((P, D, Q, M, None, None, None, None))

# Construct DataFrame from gridlist
griddataframe2 = pd.DataFrame(gridlist2, 
                        columns=['P', 'D', 'Q', 'M', 'AIC', 'BIC', 'MAE', 'T'])

print(griddataframe2, end=sp)

# Print griddataframe in order of increasing AIC
print('Based on AIC:', griddataframe2.sort_values('AIC').head(1), end=sp, sep='\n')

# Print griddataframe in order of increasing BIC
print('Based on BIC:\n', griddataframe2.sort_values('BIC').head(1), end=sp)

# Print griddataframe in order of increasing MAE
print('Based on MAE:\n', griddataframe2.sort_values('MAE').head(1), end=sp)

'''


# Detrending
# https://www.statsmodels.org/stable/examples/notebooks/generated/statespace_structural_harvey_jaeger.html
import statsmodels.api as sm

# Unrestricted model, using string specification
unrestricted_model = {
    'level': 'local linear trend', 'cycle': True, 'damped_cycle': True, 'stochastic_cycle': True
}

# The restricted model forces a smooth trend
restricted_model = {
    'level': 'smooth trend', 'cycle': True, 'damped_cycle': True, 'stochastic_cycle': True
}


# Output
output_mod = sm.tsa.UnobservedComponents(apple.loc['2016':,['Adj Close']], **unrestricted_model)
output_res = output_mod.fit(method='powell', disp=False)

# Output2
output_mod2 = sm.tsa.UnobservedComponents(apple.loc['2016':,['Adj Close']], **restricted_model)
output_res2 = output_mod2.fit(method='powell', disp=False)


fig = output_res.plot_components(legend_loc='lower right', figsize=(15, 15));
fig = output_res2.plot_components(legend_loc='lower right', figsize=(15, 15));
