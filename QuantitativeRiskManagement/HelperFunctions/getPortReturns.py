#!/usr/bin/env python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from HelperFunctions.loadData import _loadAssets

def _loadPortReturns():

    # load the asset data
    asset_prices = _loadAssets("assetsData.csv", index="Date")

    # equal weights
    n = len(asset_prices.columns)
    weights = np.repeat(1/n, n)

    # Compute the portfolio's daily returns
    asset_returns = asset_prices.pct_change().dropna()
    portfolio_returns = asset_returns.dot(weights)
    portfolio_returns.columns = "PortReturns"

    # Generate the covariance matrix from portfolio asset's returns
    covariance = asset_returns.cov()

    # Annualize the covariance using 252 trading days per year
    covariance = covariance * 252

    return portfolio_returns, asset_returns, weights, covariance