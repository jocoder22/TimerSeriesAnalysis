#!/usr/bin/env python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict

# Import the EfficientCVaR class
from pypfopt.efficient_frontier import EfficientCVaR, EfficientFrontier
from pypfopt.risk_models import CovarianceShrinkage
from pypfopt import risk_models, expected_returns


from scipy.stats import gaussian_kde

from HelperFunctions.getPortReturns import _loadPortReturns
from HelperFunctions.loadData import _loadAssets

sns.set_style("darkgrid", {"grid.color": ".6", "grid.linestyle": ":"})

sp = {"end":"\n\n\n", "sep":"\n\n\n"}

# load the asset data
assets = _loadAssets("assetsDataClose.csv", index="Date")

# # load asset and portfolio returns
portfolio_returns, asset_returns, _, _ = _loadPortReturns()
portfolio_losses = -portfolio_returns

# fit a guassian kde to the losses
fitted = gaussian_kde(portfolio_losses)

# Visualize the fitted distribution with a plot
x = np.linspace(-0.25,0.25,1000)
plt.plot(x,fitted.evaluate(x))
plt.show()

# Create a random sample of 100,000 observations from the fitted distribution
sample = fitted.resample(100000)

# Compute and display the 95% VaR from the random sample
VaR_95 = np.quantile(sample, 0.95)
print(VaR_95, **sp)

# Create the efficient frontier for CVaR minimization
ec = EfficientCVaR(None, asset_returns)

# Find the cVaR-minimizing portfolio weights at the default 95% confidence level
optimal_weights = ec.min_cvar()
print(optimal_weights, **sp)

names = {i:n for i,n in enumerate(asset_returns.columns)}

# Map the values in optimal_weights to the bank names
optimal_weights = {names[i] : optimal_weights[i] for i in optimal_weights}

# Display the optimal weights
print(optimal_weights, **sp)

# compare with mean variance Efficient portfolio (Markowitz portfolio)
e_cov = CovarianceShrinkage(assets).ledoit_wolf()

# Create the efficient frontier for Markowitz minimization
ec = EfficientFrontier(None, e_cov)

# Find the Markowit minimizing portfolio weights at the default 95% confidence level
optimal_weights_m = ec.min_volatility()

print(dict(optimal_weights_m),optimal_weights, **sp)

kk = defaultdict(list)
for f in [dict(optimal_weights_m),optimal_weights]:
    for k,v in f.items():
        kk[k].append(v)
        
# Display the optimal weights
pdd = pd.DataFrame.from_dict(kk , orient="index", columns =["Mean_Variance", "CVaR Portfolio"])
print(pdd, **sp)

# In this exercise we'll derive the 95% CVaR-minimizing portfolio 
# for 2005-2006, 2007-2008, and 2009-2010. These are the periods (or 'epochs') 
# before, during and after the crisis.
# Create a dictionary of time periods (or 'epochs')
epochs = { 'before' : {'start': '1-1-2005', 'end': '31-12-2006'},
           'during' : {'start': '1-1-2007', 'end': '31-12-2008'},
           'after'  : {'start': '1-1-2009', 'end': '31-12-2010'}
         }

# Initialize the dictionary of optimal weights
opt_wts_dict = defaultdict(list)

crisislist = ['before', 'during', 'after']
eee = {i:defaultdict(list) for i in crisislist}
print(eee, **sp)

# For each epoch, assign an efficient frontier cvar instance to ec
for x in crisislist: 
    sub_assets = assets.loc[epochs[x]['start']:epochs[x]['end'], :]
    sub_return = assets.pct_change().dropna()
    ec_dict = EfficientCVaR(None, sub_return)

    # Find and display the CVaR-minimizing portfolio weights at the default 95% confidence level
    opt_wts_dict_ = ec_dict.min_cvar()

    # For each epoch, compute efficient covariance shrinkage
    e_cov = CovarianceShrinkage(sub_assets).ledoit_wolf()

    # Create the efficient frontier for Markowitz minimization
    ec = EfficientFrontier(None, e_cov)

    # Find the Markowit minimizing portfolio weights at the default 95% confidence level
    optimal_weights_mv = dict(ec.min_volatility())

    # map bank names to optimal weights
    opt_wts_dict_cvar = {names[i] : opt_wts_dict_[i] for i in opt_wts_dict_}
    for ll in [opt_wts_dict_cvar, optimal_weights_mv]:
        for k,v in ll.items():
            eee[x][k].append(v)
            opt_wts_dict[k].append(v)

# Display the optimal weights
collist = [f"{i}_{m}" for i in crisislist for m in ["CVaR", "MV"]]
pdd2 = pd.DataFrame.from_dict(opt_wts_dict , orient="index", columns=collist)
pdd22 = pd.DataFrame.from_dict(dict(eee))
print(pdd2, pdd22,eee.values(), **sp)
