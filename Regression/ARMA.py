import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import datasets
plt.style.use('ggplot')
import datetime
import pandas_datareader as pdr

from statsmodels.tsa.arima_process import ArmaProcess
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.arima_model import ARMA

################### From Fred: contains daily data of 10-year interest rate
# https: // fred.stlouisfed.org/
starttime = datetime.datetime(1960, 1, 1)
endtime = datetime.datetime(2012, 12, 31)
interest_rate_data = pdr.DataReader('DGS10', 'fred', starttime, endtime)

interest_rate_data = interest_rate_data.resample(rule='A').last()

print(interest_rate_data['DGS10'][0])
# Forecast interest rates using an AR(1) model
mod = ARMA(interest_rate_data['DGS10'], order=(1, 0))
res = mod.fit()

# Plot the original series and the forecasted series
res.plot_predict(start=0, end='2022')
plt.legend(fontsize=8)
plt.show()





###### simulated data using ArmaProcess
ar1 = np.array([1, -1])
ma1 = np.array([1])
AR_object1 = ArmaProcess(ar1, ma1)
simulated_data_1 = AR_object1.generate_sample(nsample=len(interest_rate_data))


############### Simulated data: Random walk
np.random.seed(000)
# stimulate randon walk
steps = np.random.normal(loc=0, scale=1, size=len(interest_rate_data))

# Set first element to 0 so that the first interest rate will be the starting interest rate
steps[0]=0

# Simulate interest rate, P with a starting rate of 5
P = interest_rate_data['DGS10'][0] + np.cumsum(steps)

# Plot the interest rate series and the simulated random walk series side-by-side
fig, axes = plt.subplots(3,1)

# Plot the autocorrelation of the interest rate series in the top plot
fig = plot_acf(interest_rate_data, alpha=1, lags=12, ax=axes[0])


# Plot the autocorrelation of the simulated random walk series in the bottom plot
fig = plot_acf(simulated_data_1, alpha=1, lags=12, ax=axes[1])

# Plot the autocorrelation of the simulated random walk series in the bottom plot
fig = plot_acf(P, alpha=1, lags=12, ax=axes[2])

# Label axes
axes[0].set_title("Interest Rate Data")
axes[1].set_title("Simulated Random Walk Data, using ArmaProcess")
axes[2].set_title("Simulated Random Walk Data, using Random.Normal")
axes[0].get_xaxis().set_visible(False)
axes[1].get_xaxis().set_visible(False)
plt.show()

