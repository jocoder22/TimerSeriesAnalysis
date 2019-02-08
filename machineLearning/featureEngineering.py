import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader as pdr
from datetime import datetime
from statsmodels.tsa.arima_process import ArmaProcess
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.arima_model import ARMA
from statsmodels.graphics.tsaplots import plot_pacf

from functools import partial

stocks = ['EBAY', 'YAHOY']

startdate = datetime(2010, 1, 4)
enddate = datetime(2015, 1, 31)

portfolio = pdr.get_data_yahoo(stocks, startdate, enddate)['Adj Close']

portfolio.plot()
plt.show()


ffeatures = portfolio.rolling(30).aggregate([np.mean, np.std, np.max]).dropna()
print(ffeatures.head())


ffeatures.plot()
plt.show()


meanAlldata = partial(np.mean, axis=0)
percentileAlldata = [partial(np.percentile, q=qqt) for qqt in [25, 50, 95]]


portfolioMean = meanAlldata(portfolio)
portfolioPercentile = [f_functions(portfolio) for f_functions in percentileAlldata]







# Feature Engineering
# Define a rolling window with Pandas, excluding the right-most datapoint of the window
prices_perc_rolling = portfolio.rolling(20, min_periods=5, closed='right')

# Define the features you'll calculate for each window
features_to_calculate = [np.min, np.max, np.mean, np.std]

# Calculate these features for your rolling window object
features = prices_perc_rolling.aggregate(features_to_calculate)

# Plot the results
fig, ax = plt.subplots()
features.loc[:"2011-01"].plot(ax=ax)
portfolio.loc[:"2011-01"].plot(ax=ax, color='k', alpha=.2, lw=3)
ax.legend(loc=(1.01, .6))
plt.show()



percentiles = [1, 10, 25, 50, 75, 90, 99]

# Use a list comprehension to create a partial function for each quantile
percentile_functions = [partial(np.percentile, q=percentile)
                        for percentile in percentiles]

# Calculate each of these quantiles on the data using a rolling window
pricesrolling = portfolio.rolling(
    20, min_periods=5, closed='right')
features_percentiles = pricesrolling.aggregate(percentile_functions)
print(features_percentiles.head())


# Plot a subset of the result
features_percentiles.loc[:"2011-01", 'EBAY'].plot(cmap=plt.cm.viridis)
plt.legend(percentiles, loc=(1.01, .5))
plt.show()



portfolio['weekday'] = portfolio.index.weekday_name
portfolio['day_of_week'] = portfolio.index.dayofweek
portfolio['week_of_year'] = portfolio.index.weekofyear
portfolio['month_of_year'] = portfolio.index.month

print(portfolio.head())
