#!/usr/bin/env python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import timedelta, datetime

import statsmodels.api as sm
from statsmodels.formula.api import ols
from scipy.stats import f


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

plt.axvline(x = datetime(2008, 6, 30), c='yellow', label = "Structural Break, June 30, 2008")
plt.axvline(x = datetime(2008, 3, 31), c='black', label = "Structural Break, March 31, 2008")
plt.axvline(x = datetime(2009, 6, 30), c='white', label = "Structural Break, June 30, 2009")

# Create legend and plot
plt.legend()
plt.show()

# Build OLS model to check for structural breaks
data = pd.concat([returns_Q_min, quarterly_], axis=1, sort=False).dropna()
data.columns = ["QReturnmin", "del_rate", "mort_income_per"]

# Add a constant to the regression
del_rate = sm.add_constant(data["del_rate"])

# Regress quarterly minimum portfolio returns against mortgage delinquencies
result = sm.OLS(data["QReturnmin"], del_rate).fit()

print(result.summary(), **sp)

# Retrieve the sum-of-squared residuals
ssr_total = result.ssr
print(f"Sum-of-squared residuals, 2005-2010: {ssr_total}", **sp)

# create before and after break point data
breakpoint_ = datetime(2008, 3, 31)

before = data.loc[:breakpoint_, :]
after = data.loc[breakpoint_:, :]

# Add intercept constants to each sub-period 'before' and 'after'
before_with_intercept = sm.add_constant(before['del_rate'])
after_with_intercept  = sm.add_constant(after['del_rate'])

# Fit OLS regressions to each sub-period
r_b = sm.OLS(before['QReturnmin'], before_with_intercept).fit()
r_a = sm.OLS(after['QReturnmin'],  after_with_intercept).fit()

# Get sum-of-squared residuals for both regressions
ssr_before = r_b.ssr
ssr_after = r_a.ssr

# Compute and display the Chow test statistic
# k = 2, the degrees of freedom, number of estimated parameter, here 2, the intercept and del_rate coefficient
# the denominator, the total number of observations - (k * 2)
k = r_b.params.size
numerator = ((ssr_total - (ssr_before + ssr_after)) / k)
denominator = ((ssr_before + ssr_after) / (before.shape[0] + after.shape[0] - k * 2))
chow_stats = numerator / denominator
pvalue = f.cdf(chow_stats, numerator, denominator)

# Chow test statistic follows F-distribution
print(f"Chow test statistic: {chow_stats:.3}, P-value {pvalue:.3}", **sp)


########################## using breakpoint as categorical variables #################
breakpoint_2 = datetime(2009, 6, 30)
data.reset_index(inplace = True)

data["breakpointr"] = data["Date"].apply(lambda x: "Before" if x < breakpoint_ else "After")
data["breakpointr2"] = data["Date"].apply(lambda x: "Before" if x < breakpoint_ else 
                                            ("During" if x < breakpoint_2 else "After"))
print(data, data.info(), **sp)

# build OLS models
model = ols('QReturnmin ~ del_rate + mort_income_per + C(breakpointr)', data=data).fit()
print(model.summary(), **sp)

model2 = ols('QReturnmin ~ del_rate + mort_income_per + C(breakpointr2)', data=data).fit()
print(model2.summary(), **sp)