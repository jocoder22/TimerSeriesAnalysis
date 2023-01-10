#!/usr/bin/env python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict

# Import the EfficientCVaR class
from pypfopt.efficient_frontier import EfficientCVaR, EfficientFrontier
from pypfopt.risk_models import CovarianceShrinkage

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