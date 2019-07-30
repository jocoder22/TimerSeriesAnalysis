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

symbol = 'AAPL'
starttime = datetime(2006, 1, 1)
today = date.today()
apple = pdr.get_data_yahoo(symbol, starttime, today)


print(apple.head())

# do grid search for parameters

gridlist = []

# Loop over p values from 0-3
for p in range(4):

    # Loop over q values from 0-2
    for q in range(4):

        # Loop over for the trend values
        for t in ['n','c','t','ct']:

            try:
                # create and fit ARMA(p,q) model
                model = SARIMAX(apple['Close'], order=(p,1,q), trend=t)
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


