from sklearn.model_selection import TimeSeriesSplit
from sklearn.model_selection import ShuffleSplit
from sklearn.model_selection import KFold
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader as pdr
from datetime import datetime
from statsmodels.tsa.arima_process import ArmaProcess
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.arima_model import ARMA
from statsmodels.graphics.tsaplots import plot_pacf


# import inspect
# lines = inspect.getsource(foo)
# print(lines)


def visualize_predictions(results):
    fig, axs = plt.subplots(2, 1, sharex=True)

    # Loop through our model results to visualize them
    for idx, (prediction, score, indices) in enumerate(results):
        # Plot the predictions of the model in the order they were generated
        offset = len(prediction) * idx
        axs[0].scatter(np.arange(len(prediction)) + offset,
                       prediction, label='Iteration {}'.format(idx))

        # Plot the predictions of the model according to how time was ordered
        axs[1].scatter(indices, prediction, alpha=1/(idx + 5))
    axs[0].legend(loc="best")
    axs[0].set(xlabel="Test prediction number",
               title="Predictions ordered by test prediction number")
    axs[1].set(xlabel="Time", title="Predictions ordered by time")
    plt.show()


def visualize_predictions2(results):
    fig, axs = plt.subplots(2, 1, figsize=(10, 10), sharex=True)

    # Loop through our model results to visualize them
    for idx, (prediction, indices) in enumerate(results):
        # Plot the predictions of the model in the order they were generated
        offset = len(prediction) * idx
        axs[0].scatter(np.arange(len(prediction)) + offset,
                       prediction, label='Iteration {}'.format(idx))

        # Plot the predictions of the model according to how time was ordered
        axs[1].scatter(indices, prediction)
    axs[0].legend(loc="best")
    axs[0].set(xlabel="Test prediction number",
               title="Predictions ordered by test prediction number")
    axs[1].set(xlabel="Time", title="Predictions ordered by time")
    plt.show()





startdate = datetime(2010, 1, 4)
enddate = datetime(2015, 1, 31)

stock = pdr.get_data_yahoo('AAPL', startdate, enddate)['Adj Close']

print(stock.head())


# These are the "time lags"
shifts = np.arange(1, 8).astype(int)

# Use a dictionary comprehension to create name: value pairs, one pair per shift
shifted_stock = {"lag_{}_day".format(shifted): stock.shift(
    shifted) for shifted in shifts}

# Convert into a DataFrame for subsequent use
stock_shifted = pd.DataFrame(shifted_stock)

# Plot the first 100 samples of each
ax = stock_shifted.iloc[:100].plot(cmap=plt.cm.viridis)
stock.iloc[:100].plot(color='r', lw=2)
ax.legend(loc='best')
plt.show()


# Replace missing values with the median for each column
X = stock_shifted.fillna(np.nanmedian(stock_shifted))
y = stock.fillna(np.nanmedian(stock))


# Fit the model
model = Ridge()
model.fit(X, y)


def visualize_coefficients(coefs, names, ax):
    # Make a bar plot for the coefficients, including their names on the x-axis
    ax.bar(names, coefs)
    ax.set(xlabel='Coefficient name', ylabel='Coefficient value')

    # Set formatting so it looks nice
    plt.setp(ax.get_xticklabels(), rotation=45, horizontalalignment='right')
    return ax


# Visualize the output data up to "2011-01"
fig, axs = plt.subplots(2, 1, figsize=(10, 5))
y.loc[:'2011-01'].plot(ax=axs[0])

# Run the function to visualize model's coefficients
visualize_coefficients(model.coef_, stock_shifted.columns, ax=axs[1])
plt.tight_layout()
plt.show()

print(X[:5])
print(y[:5])
print(X.values[:5])

####################  cross validation
# Create KFold cross-validation object
cv = KFold(n_splits=10, shuffle=False, random_state=1)

# Iterate through CV splits
results = []
X = X.values
y = y.values
for tr, tt in cv.split(X, y):
    # Fit the model on training data
    model.fit(X[tr], y[tr])
    # Generate predictions on the test data and collect
    prediction = model.predict(X[tt])
    results.append((prediction, tt))




def visualize_predictions3(result):
    fig, axs = plt.subplots(2, 1)
    # xx = np.arange(len(y))
    for ix, (predictions, indices) in enumerate(result):
        offset = len(predictions) * ix
        axs[0].scatter(indices, predictions,
                c=np.arange(len(predictions)), cmap='viridis')
        # axs[1].scatter(np.arange(len(predictions)) + offset3, predictions)
        #  c=indices, cmap=plt.cm.viridis)
        axs[1].scatter(np.arange(len(predictions)),
                       predictions, label='Iteration {}'.format(ix))
    
    plt.legend()
    plt.tight_layout()
    plt.show()

    # y_test.plot(color='k', lw=3, label="Actual Prices")
    # predictions_series.plot(color='r', lw=2, label="Predicted Prices")
    # plt.title("Actual and Predicted Prices")
    # plt.legend()
    # plt.show()

# Custom function to quickly visualize predictions
visualize_predictions2(results)
visualize_predictions3(results)


cv = ShuffleSplit(n_splits=10, random_state=1)

# Iterate through CV splits
results = []
for tr, tt in cv.split(X, y):
    # Fit the model on training data
    model.fit(X[tr], y[tr])

    # Generate predictions on the test data, score the predictions, and collect
    prediction = model.predict(X[tt])
    score = r2_score(y[tt], prediction)
    results.append((prediction, score, tt))

# Custom function to quickly visualize predictions
visualize_predictions(results)


# Import TimeSeriesSplit

# Create time-series cross-validation object
cv = TimeSeriesSplit(10)

# Iterate through CV splits
fig, axs = plt.subplots(2, 1)
my_labels = {"x1": "Train", "x2": "Test"}
for idx, (tr, tt) in enumerate(cv.split(X, y)):
    # Plot the training data on each iteration, to see the behavior of the CV
    # ax.plot(tr, idx + y[tr])
    offset = idx * 10
    axs[0].plot(tr, [idx] * len(tr), c='r', label=my_labels['x1'])
    my_labels["x1"] = "_nolegend_"
    axs[0].plot(tt, [idx] * len(tt), c='g', label=my_labels['x2'])
    my_labels['x2'] = '_nolegend_'
    axs[1].plot(tr, offset + y[tr], label='Iteration {}'.format(idx))
plt.legend()
ax.set(title='Training data on each CV iteration', ylabel='CV iteration')

plt.show()
