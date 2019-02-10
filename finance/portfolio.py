import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import datasets
# plt.style.use('ggplot')
import pandas_datareader as pdr
from datetime import datetime

path = 'C:\\Users\\Jose\\Desktop\\TimerSeriesAnalysis\\finance'
os.chdir(path)
# startdate = datetime(2010,11,1)
# enddate = datetime(2019,1,30)
startdate = datetime(2013, 2, 2)
enddate = datetime(2018, 5, 30)

stocklist = ['AAPL', 'ABT', 'AIG','AMAT', 'ARNC', 'BAC', 'BSX', 'C',  'CMCSA',
             'CSCO', 'DAL', 'EBAY', 'F', 'FB', 'FCX', 'FITB', 'FOXA', 'FTR', 'GE',
             'GILD', 'GLW', 'GM', 'HAL', 'HBAN', 'JPM', 'KEY', 'HPQ', 'INTC',
             'KMI', 'KO', 'MRK', 'MRO', 'MSFT', 'MU', 'NFLX', 'NVDA', 'ORCL', 'PFE',
             'QCOM', 'RF', 'SBUX', 'T', 'V', 'VZ', 'WFC', 'XOM', 'XRX', 'YAHOY']

allstocks = pdr.get_data_yahoo(stocklist, startdate, enddate)['Adj Close']
print(allstocks.head())
allstocks.dropna()

# allstocks.to_csv('allstocks.csv')

# allstocks = pd.read_csv('allstocks.csv', parse_dates=True, index_col='Date')


# stocks = ['LNG', 'SPY', 'SMLV']
# allstocks = pdr.get_data_yahoo(stocks, startdate, enddate)['Adj Close']

# allstocks.dropna()
# print(allstocks.head())

# Resample the full dataframe to monthly timeframe
monthly_sample = allstocks.resample('BMS').first()

# Calculate daily returns of stocks
returns_daily = allstocks.pct_change()

# Calculate monthly returns of the stocks
returns_monthly = monthly_sample.pct_change().dropna()
print(returns_monthly.tail())


# Daily covariance of stocks (for each monthly period)
covariance_dict = {}
daily_index = returns_daily.index

for i in returns_monthly.index:    
    # Mask daily returns for each month and year, and calculate covariance
    mask = (daily_index.month == i.month) & (daily_index.year == i.year)
    
    # Use the mask to get daily returns for the current month and year of monthy returns index
    covariance_dict[i] = returns_daily[mask].cov()
    

print(covariance_dict[i])
print(i)


portfolio_returns, portfolio_volatility, portfolio_weights = {}, {}, {}

np.random.seed(123)
# Get portfolio performances at each month
for date in sorted(covariance_dict.keys()):
    cov = covariance_dict[date]
    for portfolio in range(200):
        weights = np.random.random(allstocks.shape[1])
        weights /= np.sum(weights) # /= divides weights by their sum to normalize 
        
        returns = np.dot(weights, returns_monthly.loc[date])
        volatility = np.sqrt(np.dot(weights.T, np.dot(cov, weights)))
        portfolio_returns.setdefault(date, []).append(returns)
        portfolio_volatility.setdefault(date, []).append(volatility)
        portfolio_weights.setdefault(date, []).append(weights)

print(portfolio_weights[date][0])

# Get latest date of available data
date = sorted(covariance_dict.keys())[-1]  

# Plot efficient frontier
# warning: this can take at least 10s for the plot to execute...
plt.scatter(portfolio_volatility[date], portfolio_returns[date], alpha=0.3)
plt.xlabel('Volatility')
plt.ylabel('Returns')
plt.show()