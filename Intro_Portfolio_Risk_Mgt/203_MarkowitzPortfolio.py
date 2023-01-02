import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict

import mmodules.header as hd

plt.style.use('fivethirtyeight')

portfolio_ = hd._getAssets(datan="2")
portfolio = portfolio_[portfolio_.index < "2020-12-31"].drop(["S&P500"], axis=1)
portfolios = hd.getEfficientPortfolio(portfolio, mYear=True)

# Plot efficient frontier
portfolios.plot.scatter(x='Volatility', y='Returns', marker='o', s=15, alpha=0.3, grid=True, figsize=[10,10])
plt.show()

# Risk free rate
risk_free = 0.0042

# Calculate the Sharpe Ratio for each asset
portfolios['Sharpe'] = (portfolios.Returns - risk_free) / portfolios["Volatility"]

# # Print the range of Sharpe ratios
# print(portfolios['Sharpe'].describe()[['min', 'max']],  **hd.sp)

# compute the asset returns
portfolio = portfolio_.pct_change().dropna()

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
# print(gmrPortfolio, gmrPortfolio.values,  **hd.sp)
GMR_weights = np.array(gmrPortfolio.values[2:11])
portfolio['Portfolio_GMR'] = np.dot(portfolio.iloc[:, 0:9], GMR_weights)

# Plot the cumulative Returns
hd.cumulative_returns_plot(portfolio[['S&P500', 'Portfolio_MSR', 'Portfolio_GMV', 'Portfolio_GMR']])

CumulativeReturns = ((1+portfolio[['S&P500', 'Portfolio_MSR', 'Portfolio_GMV', 'Portfolio_GMR']]).cumprod()-1)
trainReturns =  CumulativeReturns[CumulativeReturns.index < "2020-12-31"]
testReturns =  CumulativeReturns[CumulativeReturns.index > "2020-12-31"]

plt.subplots(figsize=(13, 10))
plt.plot(testReturns)
plt.plot(trainReturns)
plt.legend(trainReturns.columns)
plt.ylabel("Cumulative Portfolio Returns")
plt.axvspan("2020-12-31", "2022-12-31", color = 'lightblue')
plt.show()  


CumulativeReturns.plot(figsize =[12,10], title="Cumulative Returns Plot")
plt.ylabel("Cumulative Portfolio Returns")
plt.axvspan("2020-12-31", "2022-12-31", color = 'lightblue')
plt.show() 
