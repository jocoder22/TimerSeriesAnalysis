#!/usr/bin/env python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import timedelta

import statsmodels.api as sm

from HelperFunctions.getPortReturns import _loadPortReturns
from HelperFunctions.cleaners import _getCleanedData
from HelperFunctions.loadData import _loadAssets

sns.set_style("darkgrid", {"grid.color": ".6", "grid.linestyle": ":"})
sp = {"end":"\n\n\n", "sep":"\n\n\n"}

# Now you'll have a chance to investigate whether something "structural" 
# changed between 2005 and 2010. In this exercise you can see if quarterly 
# minimum portfolio values and mean return volatility time series together 
# identify a structural break.

# load the asset data
asset = _loadAssets("assetsData.csv", index="Date")
monthly_, quarterly_ = _getCleanedData()

# load asset and portfolio returns
portfolio_returns, asset_returns, _, _ = _loadPortReturns()

losses = portfolio_returns

# Calculate the 30-day rolling window of portfolio returns
returns_windowed = losses.rolling(84)

# Compute the volatility series
volatility_series = returns_windowed.std()

# Now convert daily volatility to quarterly mean volatility
vol_Q_mean = volatility_series.resample('Q').mean()

# Now convert daily returns to quarterly minimum returns
returns_Q_min = losses.resample('Q', closed="left", label="left", convention="end").min().dropna()
returns_Q_min.index = returns_Q_min.index + timedelta(days = 1)

# Now convert daily returns to quarterly max returns
returns_Q_max = losses.resample('Q').max()

# Now convert daily returns to quarterly mean returns
returns_Q_mean = losses.resample('Q').mean()

# Now convert volatility to quarterly volatility
vol_Q = losses.resample('Q').std()

measurelist = [vol_Q_mean, vol_Q, returns_Q_min, returns_Q_mean, returns_Q_max]
labels = ["Quarterly mean volatility", "Quarterly Volatility", 
        "Quarterly minimum return", "Quarterly mean return", "Quarterly max return"]

# Create the plot
for i, measure in enumerate(measurelist):
    plt.plot(measure, label=labels[i])

# Create legend and plot
plt.legend()
plt.show()

# Build OLS model to check for structural breaks
data = pd.concat([returns_Q_min, quarterly_], axis=1, sort=False).dropna()
data.columns = ["QReturnmin", "del_rate", "mort_income_per"]

# Add a constant to the regression
mort_del = sm.add_constant(data["del_rate"])

# Regress quarterly minimum portfolio returns against mortgage delinquencies
result = sm.OLS(data["QReturnmin"], mort_del).fit()

# Retrieve the sum-of-squared residuals
ssr_total = result.ssr
print(f"Sum-of-squared residuals, 2005-2010: {ssr_total}", **sp)

