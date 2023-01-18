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
from scipy import integrate

from HelperFunctions.getPortReturns import _loadPortReturns
from HelperFunctions.loadData import _loadAssets

sns.set_style("darkgrid", {"grid.color": ".6", "grid.linestyle": ":"})
sp = {"end":"\n\n\n", "sep":"\n\n\n"}
print(**sp)

def ecdf(a):
    x, counts = np.unique(a, return_counts=True)
    cusum = np.cumsum(counts)
    return x, cusum / cusum[-1]

def ecdf2(data):
    """Compute ECDF for a one-dimensional array of measurements."""
    # Number of data points: n
    n = len(data)

    # x-data for the ECDF: x
    x = np.sort(data)

    # y-data for the ECDF: y
    y = np.arange(1, n + 1) / n

    return x, y


def expect(func, lb = -np.inf):
  return integrate.quad(lambda y: func(y) * kde_p.pdf(y), a = lb, b = np.inf)[0]

def expect2(func, lb = -np.inf):
  return integrate.quad(lambda y: func(y) * skewcauchy.pdf(y, *ddt), a = lb, b = np.inf)[0]/100

# load the asset data
assets = _loadAssets("assetsDataClose.csv", index="Date")

# # load asset and portfolio returns
portfolio_returns, asset_returns, _, _ = _loadPortReturns()
losses = -portfolio_returns

# Resample the data into weekly blocks
weekly_maxima = losses.resample("W").max()

# Resample the data into monthly blocks
monthly_maxima = losses.resample("M").max()

# Resample the data into quarterly blocks
quarterly_maxima = losses.resample('Q').max()

# Plot the resulting maximas
weekly_maxima.plot(label = "Weekly Maxima")
quarterly_maxima.plot(label = "quarterly maxima")
monthly_maxima.plot(label = "Monthly Maxima")
plt.legend()
plt.show()

# Plot the log daily losses of GE over the period 2007-2009
losses = losses.loc["2007":]
losses.plot()

# Find all daily losses greater than 10%
extreme_losses = losses[losses > 0.10]

# Scatter plot the extreme losses
extreme_losses.plot(style='o')
plt.show()

# Fit extreme distribution to weekly maximum of losses
fitted = genextreme.fit(weekly_maxima)
params = t.fit(weekly_maxima)
kde_p = gaussian_kde(weekly_maxima)
ddt = skewcauchy.fit(weekly_maxima)

# Plot extreme distribution with weekly max losses historgram
x = np.linspace(min(weekly_maxima), max(weekly_maxima), 100)
plt.plot(x, genextreme.pdf(x, *fitted), label="Generalized Extreme Distribution")
plt.plot(x, t.pdf(x, *params), label="T Distribution")
plt.plot(x, kde_p.pdf(x), label="Gaussian Kernel Distribution")
# plt.plot(x,kde_p.evaluate(x), label="Gaussian Kernel Distribution")
plt.plot(x, skewcauchy.pdf(x, *ddt), label="Skew Cauchy Distribution", color="black")
plt.hist(weekly_maxima, 50, density = True, alpha = 0.3)
plt.legend()
plt.show()


x2 = np.linspace(min(weekly_maxima), max(weekly_maxima), 10000)

# Compute the 99% VaR (needed for the CVaR computation)

VaR_99_tt = t.ppf(0.99, *params)
VaR_99_T2   = np.quantile(t.rvs(size=1000, *params), 0.99)
VaR_99_kde1 = np.quantile(kde_p.resample(size=1000), 0.99)
VaR_99_kde2 = np.quantile(kde_p.pdf(x2), 0.01)
VaR_99_kde3 = np.percentile(kde_p.evaluate(x2), 100 - 99)
VaR_99_scdt = skewcauchy.ppf(0.99, *ddt)



print("####################################################33")
print(VaR_99_kde1, VaR_99_kde2, VaR_99_kde3, VaR_99_tt, VaR_99_T2, ddt,  **sp)


# Find the VaR as a quantile of random samples from the distributions
VaR_99_extreme = genextreme.ppf(0.99, *fitted)
VaR_99_T   = np.quantile(t.rvs(size=1000, *params), 0.99)
VaR_99_SCD   = np.quantile(skewcauchy.rvs(size=1000, *ddt), 0.99)
VaR_99_KDE = np.quantile(kde_p.resample(size=1000), 0.99)


# integral_T   = t.expect(lambda x: x, args = (params[0],), loc = params[1], scale = params[2], lb = VaR_99_t)
# integral_KDE3 = expect(lambda x: x, lb = VaR_99_kde)
# integral_KDE = kde_p.integrate_box_1d(VaR_99_kde,  np.inf)
# integral_KDE = kde_p.integrate_box_1d(VaR_99_KDE,  np.max(kdeSample))
# integral_KDE = kde_p.integrate_box(VaR_99_KDE,  np.max(kdeSample))

# Compute the 99% CVaR estimate
integral_GED = genextreme.expect(lambda x: x, 
           args=(fitted[0],), loc = fitted[1], scale = fitted[2], lb = VaR_99_extreme)
integral_T   = t.expect(lambda x: x, args = (params[0],), loc = params[1], scale = params[2], lb = VaR_99_T)
integral_SCD = skewcauchy.expect(lambda x: x/100.0, args = (ddt[0],), loc = ddt[1], 
            scale = ddt[2], lb = VaR_99_SCD)
integral_KDE = expect(lambda x: x, lb = VaR_99_KDE)
integral_SCD2 = expect2(lambda x: x, lb = VaR_99_SCD)

# Create the 99% CVaR estimates
CVaR_99_GED  = (1 / (1 - 0.99)) * integral_GED
CVaR_99_T   = (1 / (1 - 0.99)) * integral_T
CVaR_99_KDE = (1 / (1 - 0.99)) * integral_KDE
CVaR_99_SCD = (1 / (1 - 0.99)) * integral_SCD

# Display the results
print(f"99% CVaR for T: {CVaR_99_T:.4f},  99% CVaR for KDE: {CVaR_99_KDE:.4f}")
print(f"99% CVaR for SCD: {CVaR_99_SCD:.4f}, 99% CVaR for GED: {CVaR_99_GED:.4f}", **sp)

# Display the covering loss amount
portfolio_amt = 1000000
print(f"Reserve amount GED: ${portfolio_amt * CVaR_99_GED:,.2f}")
print(f"Reserve amount T-Dist: ${portfolio_amt * CVaR_99_T:,.2f}")
print(f"Reserve amount KDE: ${portfolio_amt * CVaR_99_KDE:,.2f}")
print(f"Reserve amount Skewed Cauchy: ${portfolio_amt * CVaR_99_SCD:,.2f}", **sp)

def plot_ecdf(a):
    x, y = ecdf2(a)
    x = np.insert(x, 0, x[0])
    y = np.insert(y, 0, 0.)
    plt.plot(x, y)
    plt.show()

plot_ecdf(kde_p.pdf(x))