#!/usr/bin/env python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from HelperFunctions.getPortReturns import _loadPortReturns
from HelperFunctions.loadData import _loadAssets
from HelperFunctions.black_scholes import BlackScholes, BsDelta

sns.set_style("darkgrid", {"grid.color": ".6", "grid.linestyle": ":"})
sp = {"end":"\n\n\n", "sep":"\n\n\n"}

# # load asset and portfolio returns
portfolio_returns, asset_returns, _, _ = _loadPortReturns()
portfolio_losses = -portfolio_returns

# load the asset data
assets = _loadAssets("assetsDataClose.csv", index="Date")

# get JPMorgan returns
JPMorgan_returns = asset_returns["JPMorgan"]

# Compute the volatility as the annualized standard deviation of JPMorgan returns
sigma = np.sqrt(252) * JPMorgan_returns.std()

# First, value the European put option using the Black-Scholes option pricing formula, 
# with a strike X of 80 and a time to maturity T of 1/2 a year. The risk-free interest 
# rate is 2% and the spot S is initially 70.
# Compute the Black-Scholes option price for this volatility
value_s = BlackScholes(S = 90, X = 80, T = 0.5, r = 0.02, 
                        sigma = sigma, option_type = "call")

# Compute the Black-Scholes option price for twice the volatility
value_2s = BlackScholes(S = 90, X = 80, T = 0.5, r = 0.02, 
                sigma = sigma * 2, option_type = "call")

# Display and compare both values
print(f"Option value for sigma: {value_s}",
      f"Option value for 2 * sigma: {value_2s}", sep="\n", end="\n\n")

# Select the first 100 observations of JPMorgan data
JPMorgan_spot = assets.loc[:assets.index[100], ["JPMorgan"]]

# Initialize the European put option values array
option_values = np.zeros(JPMorgan_spot.size)

# Iterate through JPMorgan's spot price and compute the option values
for i,S in enumerate(JPMorgan_spot.values):
    option_values[i] = BlackScholes(S = S, X = 40, T = 0.5, r = 0.02, 
                        sigma = sigma, option_type = "put")

# plot the graphs
fig, ax1 = plt.subplots(figsize = [10, 12])
plt.title("J.P Morgan Prices Vs JPMorgan Put Option Prices")
sns.lineplot(x=JPMorgan_spot.index, y= "JPMorgan", ax=ax1, label = "JPMorgan Prices", data=JPMorgan_spot)
ax1.set_ylabel("J.P Morgan Prices")
ax1.legend(loc = "upper left")

# # 2nd axes shares x-axis with 1st axes object
ax2 = ax1.twinx()
sns.lineplot(x=JPMorgan_spot.index, y= option_values, color = "red", label = "Put Option", ax=ax2)
ax2.set_ylabel("J.P Morgan Put Option Prices")
plt.show()


# Compute the Black-Scholes value at IBM spot price 70
value = BlackScholes(S = 70, X = 80, T = 0.5, r = 0.02, 
                      sigma = sigma, option_type = "put")
# Find the delta of the option at JPMorgan spot price 70
delta = BsDelta(S = 70, X = 80, T = 0.5, r = 0.02, 
                 sigma = sigma, option_type = "put")

# Find the option value change when the price of JPMorgan falls to 69.5
value_change = BlackScholes(S = 69.5, X = 80, T = 0.5, r = 0.02, 
                             sigma = sigma, option_type = "put") - value

# Show that the sum of the spot price change and the value_change 
# weighted by 1/delta is (close to) zero.
print( (69.5 - 70) + (1/delta) * value_change )
print(f"Delta: {delta}", f"1/Delta: {1/delta:.0f}", sep="\n")

# The change in the option value is called the “delta” of the option. 
# It is the derivative of the option value V with respect to the spot 
# price S. By holding an amount of the option equal to one over the 
# delta, changes in the price of the underlying stock can be offset.
#  Delta neutrality is when the total change in the portfolio's value 
#  from a change in the portfolio's asset price is zero. 



