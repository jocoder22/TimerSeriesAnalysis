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
# plt.subplots(ax3, ax4, sharex=True)

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
ax3.axes.get_xaxis().set_visible(False)
# ax3.axes.get_yaxis().set_ticks([])
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


plt.subplot(211)
AMZN['Adj Close'].plot()
plt.xlabel("")
plt.title('Amazon Adjusted Close Prices')

# Create a DataFrame of AMZN returns
AMZN_ret = AMZN.pct_change()

# Eliminate the NaN in the first row of returns
AMZN_ret = AMZN_ret.dropna()

# Run the ADF test on the return series and print out the p-value
results = adfuller(AMZN_ret['Adj Close'])
print('The p-value of the test on returns is: ' + str(results[1]))

plt.subplot(212)
AMZN_ret['Adj Close'].plot(sharex=True)

plt.title('Amazon Percentage Change Adjusted Close Prices (Returns)')
plt.show()



fig, (ax1, ax2, ax3) = plt.subplots(nrows=3)
# ax1.axes.get_xaxis().set_visible(False)
# ax1.xaxis.set_tick_params(labeltop='on')
# ax1.xaxis.set_label_position('top')
# put the major ticks at the middle of each cell
# ax.set_xticks(np.arange(data.shape[1]) + 0.5, minor=False)
# ax.set_yticks(np.arange(data.shape[0]) + 0.5, minor=False)

# # want a more natural, table-like display
# ax.invert_yaxis()
# ax.xaxis.tick_top()

# ax.set_xticklabels(column_labels, minor=False)
# ax1.set_ylabel_text = "Joshua "
# ax1.set_yticklabels([])
ax1.xaxis.tick_top()
ax2.axes.get_xaxis().set_visible(False)
# Stationality 
# plt.subplot(131)
HRB = pd.read_csv('HRB.csv', parse_dates=True, index_col='Quarter')
HRB['Earnings'].plot(ax=ax1)
ax1.set_xlabel(" ")
ax1.set_title('HRB Earnings with seasonality')
# plt.show()


# plt.subplot(132)
plot_acf(HRB, ax=ax2)
ax2.set_title('HRB Earnings autocorrelation')
# Seasonally adjust quarterly earnings
HRBsa = HRB.diff(4)

# Print the first 10 rows of the seasonally adjusted series
print(HRBsa.head(10))

# Drop the NaN data in the first three three rows
HRBsa = HRBsa.dropna()

# Plot the autocorrelation function of the seasonally adjusted series
# plt.subplot(133)
plot_acf(HRBsa, ax=ax3)
ax3.set_title('HRB Earnings autocorrelation seasonally adjusted ')
plt.show()