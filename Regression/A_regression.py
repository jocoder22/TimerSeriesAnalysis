#!/usr/bin/env python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import datasets
plt.style.use('ggplot')

from statsmodels.tsa.arima_process import ArmaProcess
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.arima_model import ARMA
from statsmodels.graphics.tsaplots import plot_pacf

sp = '\n\n'
# Plot 1: AR parameter = +0.9
plt.subplot(3,1,1)
ar1 = np.array([1, -0.9])
ma1 = np.array([1])
AR_object1 = ArmaProcess(ar1, ma1)
simulated_data_1 = AR_object1.generate_sample(nsample=1000)
plt.plot(simulated_data_1)
plt.title("AR parameter = +0.9")
plt.xticks([])

# Plot 2: AR parameter = 0.3
plt.subplot(3,1,2)
ar2 = np.array([1, -0.3])
ma2 = np.array([1])
AR_object2 = ArmaProcess(ar2, ma2)
simulated_data_2 = AR_object2.generate_sample(nsample=1000)
plt.plot(simulated_data_2)
plt.title("AR parameter = +0.3")
plt.xticks([])

# Plot 3: AR parameter = -0.9
plt.subplot(3,1,3)
ar3 = np.array([1, 0.9])
ma3 = np.array([1])
AR_object2 = ArmaProcess(ar3, ma3)
simulated_data_3 = AR_object2.generate_sample(nsample=1000)
plt.plot(simulated_data_2)
plt.title("AR parameter = -0.9")
plt.show()


####### Plotting ACF
fig, (ax1, ax2, ax3) = plt.subplots(nrows=3)
# ax1.xaxis.tick_top()
ax2.axes.get_xaxis().set_visible(False)
ax1.axes.get_xaxis().set_visible(False)

# Plot 1: AR parameter = +0.9
plot_acf(simulated_data_1, alpha=1, lags=20, ax=ax1)
ax1.set_title('AR parameter = +0.9')
# plt.show()

# Plot 2: AR parameter = +0.3
plot_acf(simulated_data_2, alpha=1, lags=20, ax=ax2)
ax2.set_title('AR parameter = +0.3')
# plt.show()

# Plot 3: AR parameter = -0.9
plot_acf(simulated_data_3, alpha=0.05, lags=20, ax=ax3)
ax3.set_title('AR parameter = -0.9')
plt.show()

################ Fitting the models
# Fit an AR(1) model to the first simulated data
mod = ARMA(simulated_data_1, order=(1, 0))
res = mod.fit()

# Print out summary information on the fit
print(res.summary())

# Print out the estimate for the constant and for phi
print("When the true phi=0.9, the estimate of phi (and the constant) are:")
print(res.params)

# Fit an AR(1) model to the second simulated data
mod = ARMA(simulated_data_2, order=(1, 0))
res = mod.fit()

# Print out the estimate for the constant and for phi
print("When the true phi=0.9, the estimate of phi (and the constant) are:")
print(res.params)

# Fit an AR(1) model to the third simulated data
mod = ARMA(simulated_data_3, order=(1, 0))
res = mod.fit()

# Print out the estimate for the constant and for phi
print("When the true phi=0.9, the estimate of phi (and the constant) are:")
print(res.params)

# Forecast the first AR(1) model
mod = ARMA(simulated_data_1, order=(1, 0))
res = mod.fit()
res.plot_predict(start=990, end=1010)
plt.show()

# https://pypi.org/project/iexfinance/
# pip3 install iexfinance
from datetime import datetime
from iexfinance.stocks import get_historical_intraday
date = datetime(2018, 11, 27)
yy = pd.DataFrame(get_historical_intraday("S", date))
print(yy.head())


# output_format: pandas will index the pandas dataframe using the minutes of the date
dd = get_historical_intraday("S", output_format='pandas')
print(dd.head(), dd.tail(), dd.info(), sep=sp)


ff = pd.DataFrame(get_historical_intraday("AAPL", date))
ff['date'] = ff['date'].astype('datetime64[ns]')
print(ff.head(20))
