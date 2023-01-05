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

# Plot the cumulative Returns and excess returns
title="Cumulative Returns Plot"
ylabel = "Cumulative Portfolio Returns"

# The Fama French 3-factor model:

# E(rp) = RF + beta(E(rm) - RF) + beta1*SMB + beta2*HML + alpha

# SMB: The small minus big factor
# beta1: Exposure to the SMB factor
# HML: The high minus low factor
# beta2: Exposure to the HML factor
# alpha: Performance which is unexplained by any other factors
# E(rp) - RF : The excess expected return of a stock or portfolio P
# E(rm)  : The excess expected return of the broad market portfolio B
# RF : The regional risk free-rate
# beta : Portfolio beta, or exposure, to the broad market portfolio B

# The HML factor is constructed by calculating the return of growth stocks, or 
# stocks with high valuations, versus the return of value stocks.
# The SMB factor is constructed by calculating the return of small-cap stocks, or 
# stocks with small market capitalizations, versus the return of large-cap stocks.

cols = ['SP_500', 'Portfolio_MSR', 'Portfolio_GMV', 'Portfolio_GMR']
regressValues = defaultdict(list)
for col in cols:
    # Define the regression formula
    regressValues['Model'].append(col)
    
    FamaFrench3f_model = smf.ols(formula=f'{col}_Excess ~ Mkt_RF + SMB + HML', data=FF_portfolio)

    # Fit the regression
    FamaFrench3f_fit = FamaFrench3f_model.fit()
    # print(FamaFrench3f_fit.summary(), **hd.sp)

    # Extract the beta
    regression_beta = FamaFrench3f_fit.params['Mkt_RF']
    regressValues["Beta"].append(round(regression_beta, 3))

    # Extract adjusted r-squared of the fitted regression
    regressValues['R squared Adjusted'].append(round(FamaFrench3f_fit.rsquared_adj, 3))

    # Extract  r-squared of the fitted regression
    regressValues['R squared'].append(round(FamaFrench3f_fit.rsquared, 3))

    # Extract the p-value of the SMB factor
    smb_pval = FamaFrench3f_fit.pvalues["SMB"]

    # If the p-value is significant, print significant
    if smb_pval < 0.05:
        significant_msg = 'significant'
    else:
        significant_msg = 'not significant'

    # Print the SMB coefficient
    smb_coeff = FamaFrench3f_fit.params["SMB"]
    print(f"The SMB coefficient of {col} is {smb_coeff:.3f}, and is {significant_msg}")

    # Calculate your portfolio alpha
    portfolio_alpha = FamaFrench3f_fit.params['Intercept']

    # Annualize your portfolio alpha
    portfolio_alpha_annualized = ((1 + portfolio_alpha) ** 252) - 1

    print(f"The Alpha of {col} is {portfolio_alpha:.3f}, and Annualise Alpha of {portfolio_alpha_annualized:.3f}", **hd.sp)


regressResults = pd.DataFrame(regressValues)
print(regressResults, **hd.sp)




