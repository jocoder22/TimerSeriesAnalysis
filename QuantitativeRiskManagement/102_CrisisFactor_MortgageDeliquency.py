#!/usr/bin/env python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import timedelta

import statsmodels.api as sm
from dateutil.relativedelta import relativedelta

from HelperFunctions.cleaners import _getCleanedData
from HelperFunctions.getPortReturns import _loadPortReturns

sp = {"end":"\n\n", "sep":"\n\n"}

# load asset and portfolio returns
portfolio_returns, asset_returns = _loadPortReturns()
monthly_, quarterly_ = _getCleanedData()

# Transform the daily portfolio_returns into quarterly average returns
portfolio_q_average = portfolio_returns.resample('Q', closed="left", label="left", convention="end").mean().dropna()
portfolio_q_average.index = portfolio_q_average.index + timedelta(days = 1)
print(portfolio_q_average.head(), **sp)

# Transform daily portfolio_returns returns into quarterly minimum returns
portfolio_q_min = portfolio_returns.resample('Q', closed="left", label="left", convention="end").min().dropna()
portfolio_q_min.index = portfolio_q_min.index + timedelta(days = 1)
print(portfolio_q_min.head(), **sp)

# concatenate all the data
data = pd.concat([portfolio_q_average, portfolio_q_min, quarterly_], axis=1, sort=False).dropna()
data.columns = ["Qmean", "Qmin", "del_rate", "mort_income_per"]
print(data.head(), **sp)

# Create a scatterplot 
fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=[10, 12], sharex=True)
sns.regplot(ax=ax1, x="del_rate", y="Qmean", data=data)
# sns.lmplot(x="del_rate", y="Qmin", data=data)
sns.regplot(ax=ax2, x="del_rate", y="Qmin", data=data)
plt.show()

# plot the join plot
sns.jointplot(x="del_rate", y="Qmean", data=data, kind="reg")
plt.show()

# plot the join plot
sns.jointplot(x="del_rate", y="Qmin", data=data, kind="reg")
plt.show()

# equal weights
n = len(asset_returns.columns)
weights = np.repeat(1/n, n)

# Generate the covariance matrix from portfolio asset's returns
covariance = asset_returns.cov()

# Annualize the covariance using 252 trading days per year
covariance = covariance * 252

# Compute and display portfolio volatility for 2008 - 2009
portfolio_variance = np.transpose(weights) @ covariance @ weights
portfolio_volatility = np.sqrt(portfolio_variance)

# Calculate the 30-day rolling window of portfolio returns
returns_windowed = portfolio_returns.rolling(30)

# Compute the annualized volatility series
volatility_series = returns_windowed.std()*np.sqrt(252)

# Transform annualized volatility into quarterly mean volatility
vol_q_mean = volatility_series.resample('Q', closed="left", label="left", convention="end").mean().dropna()
vol_q_mean.index = vol_q_mean.index + timedelta(days = 1)
print(vol_q_mean.head(), **sp)

data = pd.concat([vol_q_mean, data], axis=1, sort=False).dropna()
data.columns = ["Qvolmean", "Qmean", "Qmin", "del_rate", "mort_income_per"]
print(data.head(), **sp)

namelist = ["Qmean",  "Qmin", "Qvolmean"]
mort_del = sm.add_constant(data["del_rate"])
for n  in namelist:
    results = sm.OLS(data[n], mort_del).fit()
    rlm_model = sm.RLM(data[n], mort_del, M=sm.robust.norms.HuberT()).fit()

    # Print a summary of the results
    print(f"################################# {n} @@@@@@@@@@@@@@@ ###########################")
    print(results.summary(), rlm_model.summary(), **sp)
    print(f"################################# {n} @@@@@@@@@@@@@@@ ###########################",**sp)


portfolio_m_average = portfolio_returns.resample('M', closed="left", label="left", convention="end").mean().dropna()

portfolio_m_average.index = portfolio_m_average.index.to_period('M')
portfolio_m_average.index = portfolio_m_average.index.to_timestamp()

print(monthly_.columns, portfolio_m_average.tail(), **sp)

data2 = pd.concat([monthly_, portfolio_m_average], axis=1, sort=False).dropna()
data2.columns = ["mort_30year", "mort_del_R3090", "mort_del_R90+", "PortReturn"]
data2 = data2.reset_index()
print(data2.head(), data2.info(), **sp)

# # Add a constant to the regression
mort_del2 = sm.add_constant(data2[["mort_30year", "mort_del_R3090", "mort_del_R90+"]])

# # Create the OLS regression factor model and fit it to the data
results = sm.OLS(data2["PortReturn"], mort_del2).fit()

# Create the Robust regression factor model and fit it to the data
rlm_results = sm.RLM(data2["PortReturn"], mort_del2, M=sm.robust.norms.HuberT()).fit()

# print(rlm_results.params)
print(results.summary(), rlm_results.summary(), **sp)


namelist2 = ["mort_30year", "mort_del_R3090", "mort_del_R90+"]
mort_del3 = sm.add_constant(data2["PortReturn"])
for n  in namelist2:
    results2 = sm.OLS(data2[n], mort_del3).fit()
    rlm_model2 = sm.RLM(data2[n], mort_del3, M=sm.robust.norms.HuberT()).fit()

    # Print a summary of the results
    print(f"################################# {n} @@@@@@@@@@@@@@@ ###########################")
    print(results2.summary(), rlm_model2.summary(), **sp)
    print(f"################################# {n} @@@@@@@@@@@@@@@ ###########################",**sp)
