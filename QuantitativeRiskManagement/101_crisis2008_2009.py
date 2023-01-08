#!/usr/bin/env python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from HelperFunctions.getPortReturns import _loadPortReturns
from HelperFunctions.loadData import _loadAssets

# load the asset data
asset = _loadAssets("assetsData.csv", index="Date")

# load asset and portfolio returns
portfolio_returns, asset_returns, _, _ = _loadPortReturns()

# Select portfolio asset prices for the middle of the crisis, 2008-2009
asset_prices = asset.loc['2008-01-01':'2009-12-31', :]

# Plot portfolio's asset prices during this time
asset_prices.plot().set_ylabel("Closing Prices, USD")
plt.show()


# Plot portfolio returns
portfolio_returns.plot().set_ylabel("Daily Return, %")
plt.show()

# Generate the covariance matrix from portfolio asset's returns
covariance = asset_returns.cov()

# Annualize the covariance using 252 trading days per year
covariance = covariance * 252

# Display the covariance matrix
print(covariance)

 # equal weights
n = len(asset_prices.columns)
weights = np.repeat(1/n, n)

# Compute and display portfolio volatility for 2008 - 2009
portfolio_variance = np.transpose(weights) @ covariance @ weights
portfolio_volatility = np.sqrt(portfolio_variance)
print(portfolio_volatility)


# Calculate the 30-day rolling window of portfolio returns
returns_windowed = portfolio_returns.rolling(30)

# Compute the annualized volatility series
volatility_series = returns_windowed.std()*np.sqrt(252)

# Plot the portfolio volatility
volatility_series.plot().set_ylabel("Annualized Volatility, 30-day Window")
plt.show()

# Convert daily returns to quarterly average returns
returns_q = portfolio_returns.resample('Q').mean()

# Examine the beginning of the quarterly series
print(returns_q.head())

# Now convert daily returns to weekly minimum returns
returns_w = portfolio_returns.resample('W').min()

# Examine the beginning of the weekly series
print(returns_w.head())
