import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader as pdr
from datetime import datetime
from statsmodels.tsa.arima_process import ArmaProcess
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.arima_model import ARMA
from statsmodels.graphics.tsaplots import plot_pacf



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
