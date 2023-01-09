#!/usr/bin/env python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.stats import t, norm

from HelperFunctions.cleaners import _getCleanedData
from HelperFunctions.getPortReturns import _loadPortReturns

sp = {"end":"\n\n\n", "sep":"\n\n\n"}

# # load asset and portfolio returns
portfolio_returns, asset_returns, _, _ = _loadPortReturns()
portfolio_losses = -portfolio_returns

# Compute the mean and variance of the portfolio returns
pm = portfolio_losses.mean()
ps = portfolio_losses.std()

# fit to t distribution
params = t.fit(portfolio_losses)
print(params)

# CVaR can be expressed in:
# a: Confidence level 95,99,99.5
# b: Significance level i.e 100 - confidence level



############################ Experiment with t distribution
# Create the VaR measure at the 95% confidence level using t.ppf(), and large df
# this will approx to normal
VaR_95 = t.ppf(0.95, df=portfolio_losses.shape[0])

# Create the VaR meaasure at the 5% significance level using numpy.quantile()
draws = t.rvs(size = 100000, df=portfolio_losses.shape[0])
VaR_99 = np.quantile(draws, 0.99)

# Compare the 95% and 99% VaR
print("95% VaR: ", VaR_95, "; 99% VaR: ", VaR_99)

# Plot the t distribution histogram, 99% and 95% VaR measure
plt.hist(draws, bins = 100)
plt.axvline(x = VaR_95, c='g', label = "VaR at 95% Confidence Level")
plt.axvline(x = VaR_99, c='r', label = "VaR at 99% Confidence Level")
plt.legend(); plt.show()


############################## Real analysis #################################

# Compute the 95% VaR using the .ppf()
VaR_95 = t.ppf(0.95, *params)


# Compute the expected tail loss and the CVaR in the worst 5% of cases
tail_loss = t.expect(lambda x: x, args = (params[0],), loc = params[1], scale = params[2], lb = VaR_95)
CVaR_95 = (1 / (1 - 0.95)) * tail_loss

# Compare the 95%  VaR and 95% CVaR
print("95% VaR: ", VaR_95, "; 95% CVaR: ", CVaR_95)

# Plot the normal distribution histogram and add lines for the VaR and CVaR
plt.hist(t.rvs(size = 100000, *params),  label=f"T-df: {params[0]:.3f}", bins = 9000)
plt.hist(norm.rvs(size = 100000, loc = pm, scale = ps), bins = 100, label="Normal RVS", alpha=0.5)       
plt.xlim([-0.2, 0.2])
plt.axvline(x = VaR_95, c='g', label = "VaR, 95% confidence level")
plt.axvline(x = CVaR_95, c='r', label = "CVaR, worst 5% of outcomes")
plt.legend()
plt.show()

