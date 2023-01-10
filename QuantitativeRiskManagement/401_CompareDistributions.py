#!/usr/bin/env python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict

# Import the EfficientCVaR class
from pypfopt.efficient_frontier import EfficientCVaR, EfficientFrontier
from pypfopt.risk_models import CovarianceShrinkage

from scipy.stats import gaussian_kde, t, norm, skewnorm, genextreme, skewcauchy, exponweib, weibull_max
from sstudentt import SST

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
extreme = genextreme.fit(portfolio_losses)
ddt = skewcauchy.fit(portfolio_losses)

x = np.linspace(np.min(portfolio_losses), np.max(portfolio_losses), 1000)
plt.title("Portfolio Loss Analysis")
plt.plot(x, t.pdf(x, *params), label="T Distribution")
plt.plot(x, norm.pdf(x, *norm_), label="Normal Distribution")
plt.plot(x,fitted.evaluate(x), label="Gaussian Kernel Distribution")
plt.plot(x,skewnorm.pdf(x,*skwnorm), label="Skewed Normal Distribution")
plt.plot(x, genextreme.pdf(x, *extreme), label="Generalized Extreme Distribution")
plt.plot(x, skewcauchy.pdf(x, *ddt), label="Skew Cauchy Distribution", color="black")
plt.hist(portfolio_losses, 80, density=True, alpha=0.3)
plt.legend()
plt.show()

wklyMax = portfolio_losses.resample("w").max()
print(portfolio_losses.shape, wklyMax.shape)

# fit to t distribution
params = t.fit(wklyMax)
norm_ = norm.fit(wklyMax)
fitted = gaussian_kde(wklyMax)
skwnorm = skewnorm.fit(wklyMax)
extreme = genextreme.fit(wklyMax)
ddt = skewcauchy.fit(wklyMax)
weibull = exponweib.fit(wklyMax)
weibullmax = weibull_max.fit(wklyMax)

x = np.linspace(np.min(wklyMax), np.max(wklyMax), 1000)
plt.title("Maximum Weekly Loss Analysis")
plt.plot(x, t.pdf(x, *params), label="T Distribution")
plt.plot(x, norm.pdf(x, *norm_), label="Normal Distribution")
plt.plot(x,fitted.evaluate(x), label="Gaussian Kernel Distribution")
plt.plot(x,skewnorm.pdf(x,*skwnorm), label="Skewed Normal Distribution")
plt.plot(x, genextreme.pdf(x, *extreme), label="Generalized Extreme Distribution")
plt.plot(x, skewcauchy.pdf(x, *ddt), label="Skew Cauchy Distribution", color="black")
plt.plot(x, exponweib.pdf(x, *weibull), label="Exponential Weibull Distribution", color="white")
plt.plot(x, weibull_max.pdf(x, *weibullmax), label="Weibull Max Distribution")
plt.hist(wklyMax, 50, density=True, alpha=0.3)
plt.legend()
plt.show()