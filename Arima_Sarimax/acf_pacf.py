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


print(apple.head())

# There is upward trend in the apple close as show by the plot
fig, (ax1, ax2) = plt.subplots(2,1, figsize=(12,8))
apple.Close.plot(ax=ax1)
apple.Volume.plot(ax=ax2)
plt.show()

# let's perform statistical test: adfuller test
### this shows that there is trend 
result = adfuller(apple['Close'])
print(f'Test Statistic: {result[0]}\nP-value: {result[1]}\nCritical Values: {result[4]}')


# do one lag differencing
result = adfuller(apple['Close'].diff().dropna())
print(f'Test Statistic: {result[0]}\nP-value: {result[1]}\nCritical Values: {result[4]}')

# plot the one lag differencing
apple['Close'].diff().dropna().plot()
plt.show()

# plot the acf and pacf
apple['Close1d'] = apple['Close'].diff()
apple.dropna(inplace=True)
print(apple.head())
fig, (ax1, ax2) = plt.subplots(2,1, figsize=(12,8))
plot_acf(apple['Close1d'], lags=30, zero=False, ax=ax1)
plot_pacf(apple['Close1d'], lags=30, zero=False, ax=ax2)

plt.show()


# do grid search for parameters
# Loop over p values from 0-3
gridlist = []

for p in range(4):
    # Loop over q values from 0-2
    for q in range(4):
      
        try:
            # create and fit ARMA(p,q) model
            model = SARIMAX(apple['Close'], order=(p,1,q), trend='c')
            results = model.fit()
            
            # Print order and results
            gridlist.append((p,q, results.aic, results.bic))
            
        except:
            gridlist.append((p,q, None, None))

# Construct DataFrame from gridlist
griddataframe = pd.DataFrame(gridlist, 
                        columns=['p', 'q', 'AIC', 'BIC'])

print(griddataframe, end=sp)

# Print griddataframe in order of increasing AIC
print(griddataframe.sort_values('AIC'), end='\n\n')

# Print griddataframe in order of increasing BIC
print(griddataframe.sort_values('BIC'))


# create sarimax models with order=(0,1,0)
model = SARIMAX(apple['Close'], order=(0,1,0))
results = model.fit()

# Calculate the mean absolute error from residuals
mae0 = np.mean(np.abs(results.resid))

# Print mean absolute error
print(f'Mean absolute erorr for 0,0,0: {mae0}', end='\n\n')



# create sarimax models with order=(2,1,2)
model = SARIMAX(apple['Close'], order=(2,1,2))
results = model.fit()

# Calculate the mean absolute error from residuals
mae1 = np.mean(np.abs(results.resid))

# Print mean absolute error
print(f'Mean absolute erorr for 2,0,2: {mae1}')



# Instantiate the model
data = apple.loc[:,['Volume', 'Open']]
model = ARMA(apple['Close1d'], order=(0,0),exog=data)

# Fit the model
results = model.fit()

# Calculate the mean absolute error from residuals
mae2 = np.mean(np.abs(results.resid))

# Print mean absolute error
print(f'Mean absolute erorr for 0,0,0: {mae0}', end='\n\n')
print(f'Mean absolute erorr for 2,0,2: {mae1}',end=sp)
print(f'Mean absolute erorr for ARMA 0,0: {mae2}')