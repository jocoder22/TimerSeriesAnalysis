#!/usr/bin/env python
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader as pdr
from datetime import datetime
import seaborn as sns
from statsmodels.tsa.arima_process import ArmaProcess
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.arima_model import ARMA
from statsmodels.graphics.tsaplots import plot_pacf

# https://www.lfd.uci.edu/~gohlke/pythonlibs/
# http://blog.gregzaal.com/how-to-install-ffmpeg-on-windows/
# http://codetheory.in/how-to-convert-a-video-with-python-and-ffmpeg/
import talib

stocksname = ['LNG']
stocksname2 = ['SPY']

startdate = datetime(2016, 4, 15)
enddate = datetime(2018, 4, 10)

lng_df = pdr.get_data_yahoo(stocksname, startdate, enddate)[
    ['Adj Close', 'Volume']]

spy_df = pdr.get_data_yahoo(stocksname2, startdate, enddate)[
    ['Adj Close', 'Volume']]
spy_df.columns = ['Adj_Close', 'Volume']
lng_df.columns = ['Adj_Close', 'Volume']



lng_df['5d_close_future_pct'] = lng_df['Adj_Close'].shift(-5).pct_change(5)
lng_df['5d_close_pct'] = lng_df['Adj_Close'].pct_change(5)

spy_df['5d_future_close'] = spy_df['Adj_Close'].shift(-5)
spy_df['5d_close_future_pct'] = spy_df['5d_future_close'].pct_change(5)
spy_df['5d_close_pct'] = spy_df['Adj_Close'].pct_change(5)



feature_names = ['5d_close_pct']  # a list of the feature names for later

# Create moving averages and rsi for timeperiods of 14, 30, 50, and 200
for n in [14, 30, 50, 200]:

    # Create the moving average indicator and divide by Adj_Close
    lng_df['ma{}'.format(n)] = talib.SMA(lng_df['Adj_Close'].values,
                                      timeperiod=n) / lng_df['Adj_Close']
    # Create the RSI indicator
    lng_df[f'rsi{n}'] = talib.RSI(lng_df['Adj_Close'].values, timeperiod=n) 
    lng_df[f'rm{n}'] = lng_df['Adj_Close'].rolling(n).mean()

    # Create the moving average indicator and divide by Adj_Close
    spy_df['ma{}'.format(n)] = talib.SMA(spy_df['Adj_Close'].values,
                                      timeperiod=n) / lng_df['Adj_Close']
    # Create the RSI indicator
    spy_df[f'rsi{n}'] = talib.RSI(spy_df['Adj_Close'].values, timeperiod=n) 
    spy_df[f'rm{n}'] = spy_df['Adj_Close'].rolling(n).mean()


    # Add rsi. rollingmean and moving average to the feature name list
    feature_names.extend([f'ma{n}', f'rsi{n}', f'rm{n}'])


print(feature_names)

print(lng_df.head())
print(spy_df.head())

print(lng_df.tail())
print(spy_df.tail())



# Drop all na values
lng_df = lng_df.dropna()
spy_df = spy_df.dropna()

# Create features and targets
# use feature_names for features; 5d_close_future_pct for targets
features = lng_df[feature_names]
features2 = spy_df[feature_names]


targets = lng_df['5d_close_future_pct']
targets2 = spy_df['5d_close_future_pct']

# Create DataFrame from target column and feature columns
feat_targ_df = lng_df[['5d_close_future_pct'] + feature_names]

# Calculate correlation matrix
corrm = feat_targ_df.corr()
print(corrm)

#  Plot heatmap of correlation matrix
sns.heatmap(corrm, annot=True)
plt.yticks(rotation=0); plt.xticks(rotation=90)  # fix ticklabel directions
plt.tight_layout()  # fits plot area to the plot, "tightly"
plt.show()  # show the plot
plt.clf()  # clear the plot area

columnnames = list(corrm.columns.values)
# Create a scatter plot of the most highly correlated variable with the target
plt.scatter(np.arange(len(corrm)), corrm['5d_close_future_pct'])
for idx, (val, vname) in enumerate(zip(corrm['5d_close_future_pct'], columnnames)):
    offset = 0.05
    plt.text(idx+offset, val + offset, vname, ha='center', va='center')
plt.show()

print(list(corrm.columns.values))



plt.scatter(lng_df['ma200'], lng_df['5d_close_future_pct'])
plt.show()



# Import the statsmodels.api library with the alias sm
import statsmodels.api as sm

# Add a constant to the features
linear_features = sm.add_constant(features)

# Create a size for the training set that is 85% of the total number of samples
train_size = int(0.85 * features.shape[0])
train_features = linear_features[:train_size]
train_targets = targets[:train_size]
test_features = linear_features[train_size:]
test_targets = targets[train_size:]
print(linear_features.shape, train_features.shape, test_features.shape)


# Create the linear model and complete the least squares fit
model = sm.OLS(train_targets, train_features)
results = model.fit()  # fit the model
print(results.summary())

# examine pvalues
# Features with p <= 0.05 are typically considered significantly different from 0
print(results.pvalues)


# Scatter the predictions vs the targets with 80% transparency
plt.scatter(train_predictions, train_targets, alpha=0.2, color='b', label='train')
plt.scatter(test_predictions, test_targets, alpha=0.2, color='r', label='test')

# Plot the perfect prediction line
xmin, xmax = plt.xlim()
plt.plot(np.arange(xmin, xmax, 0.01), np.arange(xmin, xmax, 0.01), c='k')

# Set the axis labels and show the plot
plt.xlabel('predictions')
plt.ylabel('actual')
plt.legend()  # show the legend
plt.show()
