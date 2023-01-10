#!/usr/bin/env python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from HelperFunctions.getPortReturns import _loadPortReturns
from HelperFunctions.loadData import _loadAssets
from HelperFunctions.black_scholes import BlackScholes

sns.set_style("darkgrid", {"grid.color": ".6", "grid.linestyle": ":"})
sp = {"end":"\n\n\n", "sep":"\n\n\n"}

# # load asset and portfolio returns
portfolio_returns, asset_returns, _, _ = _loadPortReturns()
portfolio_losses = -portfolio_returns

# load the asset data
assets = _loadAssets("assetsDataClose.csv", index="Date")

# get JPMorgan returns
JPMorgan_returns = asset_returns["JPMorgan"]

# Compute the volatility as the annualized standard deviation of IBM returns
sigma = np.sqrt(252) * JPMorgan_returns.std()

# Compute the Black-Scholes option price for this volatility
value_s = BlackScholes(S = 90, X = 80, T = 0.5, r = 0.02, 
                        sigma = sigma, option_type = "call")

# Compute the Black-Scholes option price for twice the volatility
value_2s = BlackScholes(S = 90, X = 80, T = 0.5, r = 0.02, 
                sigma = sigma * 2, option_type = "call")

# Display and compare both values
print(f"Option value for sigma: {value_s}",
      f"Option value for 2 * sigma: {value_2s}", sep="\n")# Select the first 100 observations of IBM data


# Select the first 100 observations of JPMorgan data
JPMorgan_spot = assets.loc[:assets.index[100], ["JPMorgan"]]

# Initialize the European put option values array
option_values = np.zeros(JPMorgan_spot.size)

# Iterate through JPMorgan's spot price and compute the option values
for i,S in enumerate(JPMorgan_spot.values):
    option_values[i] = BlackScholes(S = S, X = 40, T = 0.5, r = 0.02, 
                        sigma = sigma, option_type = "put")



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

print(option_values)


