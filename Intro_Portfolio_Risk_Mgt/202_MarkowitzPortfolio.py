import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict

import mmodules.header as hd

plt.style.use('fivethirtyeight')

portfolio_ = hd._getAssets()
portfolio = portfolio_.drop(["S&P500"], axis=1)
portfolios = hd.getEfficientPortfolio(portfolio)


# Plot efficient frontier
portfolios.plot.scatter(x='Volatility', y='Returns', marker='o', s=15, alpha=0.3, grid=True, figsize=[10,10])
plt.show()


# Risk free rate
risk_free = 0.0042

# Calculate the Sharpe Ratio for each asset
portfolios['Sharpe'] = (portfolios.Returns - risk_free) / portfolios["Volatility"]

# Print the range of Sharpe ratios
print(portfolios['Sharpe'].describe()[['min', 'max']],  **hd.sp)


# compute the asset returns
portfolio = portfolio_.pct_change().dropna()

# maximum sharpe ratio porfolio
msrPortfolio = portfolios.iloc[portfolios.Sharpe.idxmax()]
print(msrPortfolio, msrPortfolio.values,  **hd.sp)
MSR_weights = np.array(msrPortfolio.values[2:11])
portfolio['Portfolio_MSR'] = portfolio.iloc[:, 0:9].mul(MSR_weights, axis=1).sum(axis=1)

# Global mininum volatility porfolio
gmvPortfolio = portfolios.iloc[portfolios.Volatility.idxmin()]
print(gmvPortfolio, gmvPortfolio.values, **hd.sp)
GMV_weights = np.array(gmvPortfolio.values[2:11])
portfolio['Portfolio_GMV'] = portfolio.iloc[:, 0:9].mul(GMV_weights, axis=1).sum(axis=1)


# Global maximum return porfolio
gmrPortfolio = portfolios.iloc[portfolios.Returns.idxmax()]
print(gmrPortfolio, gmrPortfolio.values,  **hd.sp)
GMR_weights = np.array(gmrPortfolio.values[2:11])
portfolio['Portfolio_GMR'] = portfolio.iloc[:, 0:9].mul(GMR_weights, axis=1).sum(axis=1)

# Plot the cumulative Returns
hd.cumulative_returns_plot(portfolio[['S&P500', 'Portfolio_MSR', 'Portfolio_GMV', "Portfolio_GMR"]])


# Plotting optimal portfolio
plt.subplots(figsize=(10, 10))
plt.scatter(portfolios['Volatility'], portfolios['Returns'],marker='o', alpha=0.3)
plt.scatter(msrPortfolio[1], msrPortfolio[0], color='r', marker='*', s=500)
plt.scatter(gmvPortfolio[1], gmvPortfolio[0], color='g', marker='*', s=500)
plt.scatter(gmrPortfolio[1], gmrPortfolio[0], color='y', marker='*', s=500)
plt.show()

Raversion = 5
allocation = defaultdict(list)

for rR in np.linspace(risk_free, max(portfolios['Returns']), 20):
    sdd = (rR - risk_free)/((msrPortfolio[0] - risk_free)/ msrPortfolio[1])
    utility_ = rR - (0.50 * Raversion * (sdd**2))
    allocation['utility'].append(utility_)
    allocation['alloc_x'].append(sdd)
    allocation['alloc_y'].append(rR)

allc_df = pd.DataFrame(allocation)
print(allc_df)

invest_portfolio = allc_df.iloc[allc_df["utility"].idxmax()]
print(invest_portfolio)


# Plotting optimal portfolio
plt.subplots(figsize=(10, 10))
plt.scatter(portfolios['Volatility'], portfolios['Returns'],marker='o', alpha=0.3)
plt.scatter(msrPortfolio[1], msrPortfolio[0], color='r', marker='*', s=500)
plt.scatter(gmvPortfolio[1], gmvPortfolio[0], color='black', marker='*', s=500)
plt.scatter(gmrPortfolio[1], gmrPortfolio[0], color='y', marker='*', s=500)
plt.plot(allc_df['alloc_x'], allc_df['alloc_y'], color = 'g')
plt.scatter(invest_portfolio[1], invest_portfolio[2], color = 'orange',  marker='*', s=500)
plt.text(invest_portfolio[1], invest_portfolio[2] + 0.001, rf"$A={Raversion}$", ha="center")
plt.xlim(0.02, 0.04)
plt.xlabel('Volatility')
plt.ylabel('Portfolio Returns')
plt.show()


print(portfolios[portfolios["Volatility"] == msrPortfolio[1]].values)
portfolios["p_sharpe"] = (msrPortfolio[0] - risk_free)/ msrPortfolio[1]
portfolios["sdd"]  = (portfolios["Returns"] - risk_free)/portfolios["p_sharpe"]
portfolios['utility'] = portfolios["Returns"] - (0.50 * Raversion * (portfolios["sdd"]**2))

print(portfolios.head())