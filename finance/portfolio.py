import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import datasets
# plt.style.use('ggplot')
import pandas_datareader as pdr
from datetime import datetime
from sklearn.ensemble import RandomForestRegressor


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



# Empty dictionaries for sharpe ratios and best sharpe indexes by date
sharpe_ratio, max_sharpe_idxs = {}, {}

# Loop through dates and get sharpe ratio for each portfolio
for date in portfolio_returns.keys():
    for i, ret in enumerate(portfolio_returns[date]):
    
        # Divide returns by the volatility for the date and index, i
        sharpe_ratio.setdefault(date, []).append(ret / portfolio_volatility[date][i])

    # Get the index of the best sharpe ratio for each date
    max_sharpe_idxs[date] = np.argmax(sharpe_ratio[date])

print(portfolio_returns[date][max_sharpe_idxs[date]])



# Calculate exponentially-weighted moving average of daily returns
ewma_daily = returns_daily.ewm(span=30).mean()

# Resample daily returns to first business day of the month with average for that month
ewma_monthly = ewma_daily.resample('BMS').first()

# Shift ewma for the month by 1 month forward so we can use it as a feature for future predictions 
ewma_monthly = ewma_monthly.shift(1).dropna()

print(ewma_monthly.iloc[-1])


targets, features = [], []

# Create features from price history and targets as ideal portfolio
for date, ewma in ewma_monthly.iterrows():

    # Get the index of the best sharpe ratio
    best_idx = max_sharpe_idxs[date]
    targets.append(portfolio_weights[date][best_idx])
    features.append(ewma)  # add ewma to features

targets = np.array(targets)
features = np.array(features)
print(targets[-5:])

# Get most recent (current) returns and volatility
date = sorted(covariance_dict.keys())[-1]
cur_returns = portfolio_returns[date]
cur_volatility = portfolio_volatility[date]

# Plot efficient frontier with sharpe as point
plt.scatter(x=cur_volatility, y=cur_returns, alpha=0.6, color='blue')
best_idx = max_sharpe_idxs[date]

# Place an orange "X" on the point with the best Sharpe ratio
plt.scatter(x=cur_volatility[best_idx], y=cur_returns[best_idx], marker='x', color='orange')
plt.xlabel('Volatility')
plt.ylabel('Returns')
plt.show()


# Make train and test features
train_size = int(0.85 * features.shape[0])
train_features = features[:train_size]
test_features = features[train_size:]
train_targets = targets[:train_size]
test_targets = targets[train_size:]

# Fit the model and check scores on train and test
# fit a randomforest tree model
rfr = RandomForestRegressor(n_estimators=300, random_state=42)
rfr.fit(train_features, train_targets)
print(rfr.score(train_features, train_targets))
print(rfr.score(test_features, test_targets))



train_predictions = rfr.predict(train_features)
test_predictions = rfr.predict(test_features)

# Calculate and plot returns from our RF predictions and the FCX returns
test_returns = np.sum(returns_monthly.iloc[train_size:] * test_predictions, axis=1)
plt.plot(test_returns, label='algo')
plt.plot(returns_monthly['FCX'].iloc[train_size:], label='FCX')
plt.legend()
plt.show()



# Calculate the effect of our portfolio selection on a hypothetical $1k investment
cash = 1000
algo_cash, FCX_cash = [cash], [cash]  # set equal starting cash amounts
for r in test_returns:
    cash *= 1 + r
    algo_cash.append(cash)

# Calculate performance for FCX
cash = 1000  # reset cash amount
for r in returns_monthly['FCX'].iloc[train_size:]:
    cash *= 1 + r
    FCX_cash.append(cash)

print('algo returns:', (algo_cash[-1] - algo_cash[0]) / algo_cash[0])
print('FCX returns:', (FCX_cash[-1] - FCX_cash[0]) / FCX_cash[0])

# Plot the algo_cash and FCX_cash to compare overall returns
plt.plot(algo_cash, label='algo')
plt.plot(FCX_cash, label='FCX')
plt.legend()  # show the legend
plt.show()


