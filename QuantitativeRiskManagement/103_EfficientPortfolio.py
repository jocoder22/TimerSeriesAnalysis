#!/usr/bin/env python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Import the mean_historical_return method
from pypfopt.expected_returns import mean_historical_return
from pypfopt.risk_models import CovarianceShrinkage
from pypfopt.cla import CLA

from HelperFunctions.loadData import _loadAssets

sp = {"end":"\n\n\n", "sep":"\n\n\n"}

# load the asset data
assets = _loadAssets("assetsDataClose.csv", index="Date")
print(assets.tail(), **sp)

# Compute the annualized average historical return
mean_returns = mean_historical_return(assets, frequency = 252)
print(mean_returns)

# Plot the annualized average historical return
plt.plot(mean_returns, linestyle = 'None', marker = 'o')
plt.show()

# Create the CovarianceShrinkage instance variable
cs = CovarianceShrinkage(assets)

# Compute the sample covariance matrix of returns
sample_cov = assets.pct_change().cov() * 252

# Compute the efficient covariance matrix of returns
e_cov = cs.ledoit_wolf()

# Display both the sample covariance_matrix and the efficient e_cov estimate
print("Sample Covariance Matrix\n", sample_cov, "\n\n")
print("Efficient Covariance Matrix\n", e_cov, "\n\n")

# Create a dictionary of time periods (or 'epochs')
epochs = { 'before' : {'start': '1-1-2005', 'end': '31-12-2006'},
           'during' : {'start': '1-1-2007', 'end': '31-12-2008'},
           'after'  : {'start': '1-1-2009', 'end': '31-12-2010'}
         }

# Compute the efficient covariance for each epoch
e_cov = {}
meanr = {}
for x in epochs.keys():
    sub_price = assets.loc[epochs[x]['start']:epochs[x]['end'], :]
    meanr[x] = mean_historical_return(sub_price, frequency = 252)
    e_cov[x] = CovarianceShrinkage(sub_price).ledoit_wolf()

    # Display the efficient covariance matrices for  epochs
    print(f"Efficient Covariance Matrices: {x}\n", e_cov[x], "\n\n")

# {x: CovarianceShrinkage(assets.loc[epochs[x]['start']:epochs[x]['end'], :]).ledoit_wolf() for x in epochs.keys()}

colors = ["b", "r", "g"]
fig, axs = plt.subplots(4, 1, figsize=(5, 10))
for n, i in enumerate(epochs.keys()):
    # Initialize the Crtical Line Algorithm object
    efficient_portfolio_during = CLA(meanr[i], e_cov[i])

    # Find the minimum volatility portfolio weights and display them
    print(f"Minimum volatility portfolio weights: {i} Crisis\n", 
                efficient_portfolio_during.min_volatility(), "\n\n")

    # Compute the efficient frontier
    (ret, vol, weights) = efficient_portfolio_during.efficient_frontier()

    # Add the frontier to the plot showing the 'before' and 'after' frontiers
    axs[0].scatter(x = vol, y = ret, s = 8, c = colors[n], marker = '*', label = f'{i}')
    axs[n+1].scatter(vol, ret, s = 8, c = colors[n], marker = '*', label = f'{i}')

    axs[0].legend()
    axs[n+1].legend()
plt.tight_layout()
plt.show()