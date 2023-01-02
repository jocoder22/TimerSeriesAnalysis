import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict

import mmodules.header as hd

plt.style.use('fivethirtyeight')

portfolio_ = hd._getAssets(datan="2")
portfolio = portfolio_[portfolio_.index < "2020-12-31"].drop(["S&P500"], axis=1)
portfolios = hd.getEfficientPortfolio(portfolio, mYear=True)

# # get fred risk free rate
# riskFree_rate = pd.read_pickle(os.path.join(hd.datapath, "fred_rfr.pkl"))
# print(riskFree_rate.head(), portfolios_.head(), **hd.sp)

# # merge the data sets
# portfolios = portfolios_.merge(riskFree_rate, on="Date", how="inner",  suffixes=(False, False))

# Plot efficient frontier
portfolios.plot.scatter(x='Volatility', y='Returns', marker='o', s=15, alpha=0.3, grid=True, figsize=[10,10])
plt.show()

# Risk free rate
risk_free = 0.00042

# Calculate the Sharpe Ratio for each asset
portfolios['Sharpe'] = (portfolios.Returns - risk_free) / portfolios["Volatility"]

# # Print the range of Sharpe ratios
# print(portfolios['Sharpe'].describe()[['min', 'max']],  **hd.sp)

# compute the asset returns
portfolio_train = portfolio_[portfolio_.index < "2020-12-31"]
portfolio_test = portfolio_[portfolio_.index > "2020-12-31"]
portfolio = portfolio_train.pct_change().dropna()

# maximum sharpe ratio porfolio
msrPortfolio = portfolios.iloc[portfolios.Sharpe.idxmax()]
MSR_weights = np.array(msrPortfolio.values[2:11])
portfolio['Portfolio_MSR'] = np.dot(portfolio.iloc[:, 0:9], MSR_weights)

# Global mininum volatility porfolio
gmvPortfolio = portfolios.iloc[portfolios.Volatility.idxmin()]
GMV_weights = np.array(gmvPortfolio.values[2:11])
portfolio['Portfolio_GMV'] = np.dot(portfolio.iloc[:, 0:9], GMV_weights)


# Global maximum return porfolio
gmrPortfolio = portfolios.iloc[portfolios.Returns.idxmax()]
print(gmrPortfolio, gmrPortfolio.values,  **hd.sp)
GMR_weights = np.array(gmrPortfolio.values[2:11])
portfolio['Portfolio_GMR'] = np.dot(portfolio.iloc[:, 0:9], GMR_weights)


# save the MSR and GMV weights
msrPortfolio.to_pickle(os.path.join(hd.datapath, 'MSR_weights.pkls'))
gmvPortfolio.to_pickle(os.path.join(hd.datapath, 'GMV_weights.pkls'))
gmrPortfolio.to_pickle(os.path.join(hd.datapath, 'GMR_weights.pkls'))


# Plot the cumulative Returns on train data
title="Train Data: Cumulative Returns Plot"
ylabel = "Cumulative Portfolio Returns"
hd.cumulative_returns_plot(portfolio[['S&P500', 'Portfolio_MSR', 'Portfolio_GMV', 'Portfolio_GMR']],
            title=title, ylabel=ylabel)

# plot cumulative Return on test data
portfolio2 = portfolio_test.pct_change().dropna()
portfolio2['Portfolio_MSR'] = np.dot(portfolio2.iloc[:, 0:9], MSR_weights)
portfolio2['Portfolio_GMV'] = np.dot(portfolio2.iloc[:, 0:9], GMV_weights)
portfolio2['Portfolio_GMR'] = np.dot(portfolio2.iloc[:, 0:9], GMR_weights)

title="Test Data: Cumulative Returns Plot"
hd.cumulative_returns_plot(portfolio2[['S&P500', 'Portfolio_MSR', 'Portfolio_GMV', 'Portfolio_GMR']],
            title=title, ylabel=ylabel)