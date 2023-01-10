#!/usr/bin/env python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict

# Import the EfficientCVaR class
from pypfopt.efficient_frontier import EfficientCVaR, EfficientFrontier
from pypfopt.risk_models import CovarianceShrinkage

from scipy.stats import gaussian_kde, t, norm, skewnorm

from HelperFunctions.getPortReturns import _loadPortReturns
from HelperFunctions.loadData import _loadAssets

sns.set_style("darkgrid", {"grid.color": ".6", "grid.linestyle": ":"})
sp = {"end":"\n\n\n", "sep":"\n\n\n"}

# load the asset data
assets = _loadAssets("assetsDataClose.csv", index="Date")

# # load asset and portfolio returns
portfolio_returns, asset_returns, _, _ = _loadPortReturns()
portfolio_losses = -portfolio_returns

# fit to t distribution
params = t.fit(portfolio_losses)
norm_ = norm.fit(portfolio_losses)
fitted = gaussian_kde(portfolio_losses)
skwnorm = skewnorm.fit(portfolio_losses)

x = np.linspace(np.min(portfolio_losses), np.max(portfolio_losses), 1000)
plt.plot(x, t.pdf(x, *params), label="T Distribution")
plt.plot(x, norm.pdf(x, *norm_), label="Normal Distribution")
plt.plot(x,fitted.evaluate(x), label="Gaussian Kernel Distribution")
plt.plot(x,skwnorm.pdf(x), label="Skewed Normal Distribution")
plt.hist(portfolio_losses, 50, density=True, alpha=0.3)
plt.legend()
plt.show()