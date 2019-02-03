import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import datetime
import pandas_datareader as pdr


from statsmodels.tsa.stattools import acf
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.stattools import adfuller

path = 'C:\\Users\\Jose\\Desktop\\TimerSeriesAnalysis'
os.chdir(path)

# starttime = datetime.datetime(1997, 5, 15)
# endtime = datetime.datetime(2017, 8, 2)

# symbol = 'AMZN'
# AMZN = pdr.get_data_yahoo(symbol, starttime, endtime)
AMZN = pd.read_csv('AMZN.csv', parse_dates=True, index_col='Date')


fig, axs = plt.subplots(nrows=2, ncols=2)
ax1, ax2, ax3, ax4 = axs[0, 0], axs[1, 0], axs[0, 1], axs[1, 1]
################## White Noise

# Simulate white noise returns
returns = np.random.normal(loc=0.02, scale=0.05, size=1000)

# Print out the mean and standard deviation of returns
mean = np.mean(returns)
std = np.std(returns)
print("The mean is %5.3f and the standard deviation is %5.3f" %(mean,std))

# Plot returns series
ax1.plot(returns)
ax1.set_title("Simple Random Noise")
# plt.show()

# Plot autocorrelation function of white noise returns
# plt.subplot(222)
plot_acf(returns, lags=20, ax=ax2)
ax2.set_title('Autocorrelated White Noise')
# plt.show()


############### Simulate stock prices
# Generate 500 random steps with mean=0 and standard deviation=1
steps = np.random.normal(loc=0, scale=1, size=500)

# Set first element to 0 so that the first price will be the starting stock price
steps[0]=0

# Simulate stock prices, P with a starting price of 100
P = 100 + np.cumsum(steps)

# Plot the simulated stock prices
# plt.subplot(223)
ax3.plot(P)
ax3.set_title("Simulated Random Walk")
# plt.show()


# Generate 500 random steps
steps = np.random.normal(loc=0.001, scale=0.01, size=500) + 1

# Set first element to 1
steps[0]=1

# Simulate the stock price, P, by taking the cumulative product
P = 100 * np.cumprod(steps)

# Plot the simulated stock prices
# plt.subplot(224)
ax4.plot(P)
ax4.set_title("Simulated Random Walk with Drift")
plt.show()


############# adfuller test for random noise (null hypothesis --> this is a random noise)
# Run the ADF test on the price series and print out the results
results = adfuller(AMZN['Adj Close'])
print(results)

# Just print out the p-value
print('The p-value of the test on prices is: ' + str(results[1]))


plt.subplot(121)
AMZN['Adj Close'].plot()
plt.title('Amazon Adjusted Close prices')

# Create a DataFrame of AMZN returns
AMZN_ret = AMZN.pct_change()

# Eliminate the NaN in the first row of returns
AMZN_ret = AMZN_ret.dropna()

# Run the ADF test on the return series and print out the p-value
results = adfuller(AMZN_ret['Adj Close'])
print('The p-value of the test on returns is: ' + str(results[1]))

plt.subplot(122)
AMZN_ret['Adj Close'].plot()
plt.title('Amazon percentage change (returns)')
plt.show()


# Stationality 
plt.subplot(131)
HRB = pd.read_csv('HRB.csv', parse_dates=True, index_col='Quarter')
HRB['Earnings'].plot()
plt.title('HRB Earnings with seasonality')
# plt.show()


plt.subplot(132)
plot_acf(HRB)
plt.title('HRB Earnings autocorrelation')
# Seasonally adjust quarterly earnings
HRBsa = HRB.diff(4)

# Print the first 10 rows of the seasonally adjusted series
print(HRBsa.head(10))

# Drop the NaN data in the first three three rows
HRBsa = HRBsa.dropna()

# Plot the autocorrelation function of the seasonally adjusted series
plt.subplot(133)
plot_acf(HRBsa)
plt.title('HRB Earnings autocorrelation seasonally adjusted ')
plt.show()