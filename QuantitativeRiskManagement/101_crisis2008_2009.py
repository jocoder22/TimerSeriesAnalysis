#!/usr/bin/env python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from HelperFunctions.loadData import _loadAssets

# load the asset data
portfolio = _loadAssets()

# Select portfolio asset prices for the middle of the crisis, 2008-2009
asset_prices = portfolio.loc['2008-01-01':'2009-12-31', :]

# Plot portfolio's asset prices during this time
asset_prices.plot().set_ylabel("Closing Prices, USD")
plt.show()

# equal weights
n = len(portfolio.columns)
weights = np.repeat(1/n, n)

# Compute the portfolio's daily returns
asset_returns = asset_prices.pct_change()
portfolio_returns = asset_returns.dot(weights)

# Plot portfolio returns
portfolio_returns.plot().set_ylabel("Daily Return, %")
plt.show()