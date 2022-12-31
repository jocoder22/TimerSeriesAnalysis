import numpy as np
import matplotlib.pyplot as plt
import mmodules.header as hd

plt.style.use('fivethirtyeight')

portfolio_ = hd._getAssets()
portfolio = portfolio_.drop(["S&P500"], axis=1)
portfolios = hd.getEfficientPortfolio(portfolio)

# Plot efficient frontier
portfolios.plot.scatter(x='Volatility', y='Returns', marker='o', s=15, alpha=0.3, grid=True, figsize=[10,10])
plt.show()


# Risk free rate
risk_free = 0

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
plt.scatter(portfolios['Volatility'], portfolios['Returns'],marker='o', s=15, alpha=0.3)
plt.scatter(msrPortfolio[1], msrPortfolio[0], color='r', marker='*', s=500)
plt.scatter(gmvPortfolio[1], gmvPortfolio[0], color='g', marker='*', s=500)
plt.scatter(gmrPortfolio[1], gmrPortfolio[0], color='y', marker='*', s=500)
plt.show()