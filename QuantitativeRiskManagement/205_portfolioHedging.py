#!/usr/bin/env python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from HelperFunctions.getPortReturns import _loadPortReturns
from HelperFunctions.black_scholes import BlackScholes

sns.set_style("darkgrid", {"grid.color": ".6", "grid.linestyle": ":"})
sp = {"end":"\n\n\n", "sep":"\n\n\n"}

# # load asset and portfolio returns
portfolio_returns, asset_returns, _, _ = _loadPortReturns()
portfolio_losses = -portfolio_returns

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
      f"Option value for 2 * sigma: {value_2s}", sep="\n")
