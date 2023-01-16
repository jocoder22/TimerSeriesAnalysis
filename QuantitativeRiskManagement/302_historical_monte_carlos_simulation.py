#!/usr/bin/env python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Import the Normal distribution and skewness test from scipy.stats
from scipy.stats import norm, t, skewcauchy

# Import the EfficientCVaR class
from pypfopt.efficient_frontier import EfficientCVaR, EfficientFrontier
from pypfopt.risk_models import CovarianceShrinkage
from pypfopt import risk_models, expected_returns

from HelperFunctions.getPortReturns import _loadPortReturns
from HelperFunctions.loadData import _loadAssets

sns.set_style("darkgrid", {"grid.color": ".6", "grid.linestyle": ":"})

sp = {"end":"\n\n\n", "sep":"\n\n\n"}

# load the asset data
assets = _loadAssets("assetsDataClose.csv", index="Date")

# # load asset and portfolio returns
portfolio_returns, asset_returns, weights, _ = _loadPortReturns()
losses = -portfolio_returns

data20052006 = assets.loc["2005":"2006", :]
data20072008 = assets.loc["2007":"2008", :]

asset_returns = [x.pct_change().dropna() for x in [data20052006, data20072008]]

# look at asset returns standard deviations
# for x in asset_returns:
#     print(x.describe(), **sp)

# Create portfolio returns for the two sub-periods using the list of asset returns
portfolio_returns = np.array([ x.dot(weights) for x in asset_returns], dtype=object)

# Derive portfolio losses from portfolio returns
losses = - portfolio_returns

# Find the historical simulated VaR estimates
VaR_95 = [np.quantile(x, 0.95) for x in losses]

# Display the VaR estimates
print(f"VaR_95, 2005-2006: {VaR_95[0]};  VaR_95, 2007-2009: {VaR_95[1]}", **sp)

# VaR estimates are very different for the two time periods. This indicates that
#  over the entire 2005 - 2009 period the loss distribution was likely not stationary. 
#  Historical simulation, while very general, should be used with caution when the 
#  data is not from a stationary distribution.

####################### Monte carlo simulation ##################################
############## using portfolio returns ##########################################
totalsteps = 60 * 24   # total minutes in a day
N = 10000            # number of simulations

mu = losses[0].mean()
sigma = losses[0].std()

# Initialize daily cumulative loss for the assets, across N runs
daily_loss = np.zeros(N)

# Create the Monte Carlo simulations for N runs
for n in range(N):
    # rvs draw by normal standard normal distribution
    # This is then scaled using 'sigma' and the time interval, and finally shifted using
    # 'mu' and the time interval. This is a way to transform a standard Normal draw to 
    # match the loss distribution.

    loss = (mu * (1/totalsteps) + norm.rvs(size = totalsteps) * sigma * np.sqrt(1/totalsteps))
    daily_loss[n] = sum(loss) # this give one daily loss by adding up the minute by minute draws

var95 = np.quantile(daily_loss, 0.95)

print(f"Monte Carlo VaR 95 estimate using Portfolio Returns: {var95}")
# Monte Carlo VaR 95 estimate using Portfolio Returns: 0.014478257481936043 => 1 million simulations

####################### Monte carlo simulation #####################################
############## using the portfolio Assets ##########################################
# Calculate expected returns and sample covariance using PyPortfolioOpt
N = 1000000            # number of simulations
mu = expected_returns.mean_historical_return(assets)
S = risk_models.sample_cov(assets)
e_cov = CovarianceShrinkage(assets).ledoit_wolf()

### Here we will use daily continous means and covariance matrix not annualized
Assetreturns = assets.pct_change().dropna()
daily_cov = Assetreturns.cov()

# formular for continous mean:
#     (1+returns)*prod() ** (freq/returns.count()) - 1
daily_mean_ = (1 + Assetreturns).prod() ** (1/Assetreturns.count()) - 1  ## here freq is equal to 1
daily_mean = np.array(daily_mean_.values).reshape(4,-1)

# Initialize daily cumulative loss for the assets, across N runs
daily_loss2 = np.zeros((4,N))

# # Create the Monte Carlo simulations for N runs
for n in range(N):
    # Compute simulated path of length total_steps for correlated returns
    correlated_randomness = daily_cov @ norm.rvs(size = (4,totalsteps))

    # Adjust simulated path by total_steps and mean of portfolio losses
    steps = 1/totalsteps
    minute_losses = daily_mean * steps + correlated_randomness * np.sqrt(steps)
    daily_loss2[:, n] = minute_losses.sum(axis=1)
    
# Generate the 95% VaR estimate
losses = weights @ daily_loss2
print(f"Monte Carlo VaR 95 estimate using Portfolio Assets: {np.quantile(losses, 0.95):.4f}", **sp)
# Monte Carlo VaR 95 estimate using Portfolio Assets: 0.000000000 => 1,440,000,000 simulations
# Monte Carlo VaR 95 estimate using Portfolio Assets: 0.0032 => 144,000,000 simulations