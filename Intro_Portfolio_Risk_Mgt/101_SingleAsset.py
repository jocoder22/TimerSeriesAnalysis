#!/usr/bin/env python
import numpy as np
import pandas as pd

# Import skew. kurtosis from scipy.stats
from scipy.stats import skew, kurtosis

from printdescribe import changepath
from mmodules.plotting import plotReturn, plotReturnHistogram

datapath = r"E:\TimerSeriesAnalysis\Intro_Portfolio_Risk_Mgt\Data"

sp = {"end":"\n\n", "sep":"\n\n"}

with changepath(datapath):
    data = pd.read_csv("portfolio.csv", index_col="Date")
    amazon = data[["Amazon"]]
    amazon.columns = ["AdjClose"]
    
print(amazon.head())

# compute simple returns
amazon["Returns"] = amazon['AdjClose'].pct_change()

# view head
print(amazon.head())

# plot the Adjusted closing price
plotReturn(amazon['AdjClose'])

# plot the returns
plotReturn(amazon['Returns'])

# Convert the decimal returns into percentage returns
percent_return = amazon['Returns']*100

# Drop the missing values
returns_plot = percent_return.dropna()

# Plot the returns histogram
plotReturnHistogram(returns_plot)

# Calculate the average daily return of the stock
mean_return_daily = np.mean(amazon['Returns'])
print(f"Mean daily returns: {mean_return_daily}")

# Calculate the implied annualized average return
mean_return_annualized = ((1+mean_return_daily)**252)-1
print(f"Annualized mean returns: {mean_return_annualized}")

# Calculate the standard deviation of daily return of the stock
sigma_daily = np.std(amazon['Returns'])
print(f"standard deviation of daily return: {sigma_daily}")

# Calculate the daily variance
variance_daily = sigma_daily ** 2
print(f"Variance of daily return: {variance_daily}")

# Annualize the standard deviation
sigma_annualized = sigma_daily*np.sqrt(252)
print(f"Annualize standard deviation: {sigma_annualized}")

# Calculate the annualized variance
variance_annualized = sigma_annualized ** 2
print(f"Annualized variance: {variance_annualized}")

# Drop the missing values
clean_returns = amazon["Returns"].dropna()

# Calculate the third moment (skewness) of the returns distribution
returns_skewness = skew(clean_returns)
print(f"Third moment (skewness): {returns_skewness}")

# Calculate the excess kurtosis of the returns distribution
excess_kurtosis = kurtosis(clean_returns)
print(f"Excess kurtosis of Returns: {excess_kurtosis}")

# Derive the true fourth moment of the returns distribution
fourth_moment = excess_kurtosis + 3.0
print(f"The true fourth moment: {fourth_moment}")
