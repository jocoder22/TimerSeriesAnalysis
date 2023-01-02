import os
import numpy as np
import pandas as pd
from collections import defaultdict

# Import statsmodels.formula.api
import statsmodels.formula.api as smf 

import mmodules.header as hd

# get our Fama French portfolio data
FF_portfolio = pd.read_pickle(os.path.join(hd.datapath, "Fama_French_PortfolioFull.pkl"))
FF_portfolio["Mkt_RF"] = FF_portfolio["Mkt-RF"]
FF_portfolio["SP_500_Excess"] = FF_portfolio["S&P500_Excess"]
# print(FF_portfolio.head(), FF_portfolio.tail(), FF_portfolio.columns, **hd.sp)

# dropcolumns = FF_portfolio.columns[4:10]
# data1 = FF_portfolio.drop(columns=dropcolumns)

# Plot the cumulative Returns and excess returns
title="Cumulative Returns Plot"
ylabel = "Cumulative Portfolio Returns"
cols = ['S&P500', 'Portfolio_MSR', 'Portfolio_GMV', 'Portfolio_GMR']
for col in cols:
    hd.cumulative_returns_plot(FF_portfolio[[col, col+"_Excess"]], title=title +f": {col} vs {col}_Excess", ylabel=ylabel)


portfolioValues = defaultdict(list)
for col in cols:
    # Calculate the co-variance matrix between Portfolio_Excess and Market_Excess
    covariance_matrix = FF_portfolio[[col+'_Excess', 'Mkt-RF']].cov()

    # Extract the co-variance co-efficient
    covariance_coefficient = covariance_matrix.iloc[0, 1]
    portfolioValues['cov_coefficient'].append(round(covariance_coefficient, 3))

    # Calculate the benchmark variance
    benchmark_variance = FF_portfolio['Mkt-RF'].var()
    portfolioValues['benchmark_variance'].append(round(benchmark_variance, 3))

    # Calculating the portfolio market beta
    portfolio_beta = covariance_coefficient/benchmark_variance
    portfolioValues["beta"].append(round(portfolio_beta, 3))
    # print(f"Beta for {col}: {portfolio_beta}")

datavalues = pd.DataFrame(portfolioValues).T
datavalues.columns = cols
print(datavalues, **hd.sp)

# Calculating beta with CAPM
# There are many ways to model stock returns, but the Capital Asset Pricing Model, 
# or CAPM, is one the most well known:

# E(rp) - RF = beta(E(rm) - RF)

# E(rp) - RF : The excess expected return of a stock or portfolio P
# E(rm)  : The excess expected return of the broad market portfolio B
# RF : The regional risk free-rate
# beta : Portfolio beta, or exposure, to the broad market portfolio B

cols = ['SP_500', 'Portfolio_MSR', 'Portfolio_GMV', 'Portfolio_GMR']
regressValues = defaultdict(list)
for col in cols:
    # Define the regression formula
    regressValues['Model'].append(col)
    CAPM_model = smf.ols(formula=f'{col}_Excess ~ Mkt_RF', data=FF_portfolio)

    # Extract the beta
    CAPM_fit = CAPM_model.fit()
    regression_beta = CAPM_fit.params['Mkt_RF']
    regressValues["Beta"].append(regression_beta)

    # Extract adjusted r-squared of the fitted regression
    regressValues['R squared Adjusted'].append(CAPM_fit.rsquared_adj)

    # Extract  r-squared of the fitted regression
    regressValues['R squared'].append(CAPM_fit.rsquared)

regressResults = pd.DataFrame(regressValues)
print(regressResults, **hd.sp)



