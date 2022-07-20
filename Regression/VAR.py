
from cmath import e
import numpy as np
import pandas as np
import matplotlib.pyplot as plt
from stationarity.stationarity_conversion import stationarityTest
import statsmodels.api as sm
from statsmodels.tsa.api import VAR

import yfinance as yf

from stationarity.stationarity_conversion import  stationarityTest


sp = {"sep":"\n\n", "end":"\n\n"}

#  load the dataset
eVgo = yf.download('EVGO')[["Adj Close", "Volume"]]

print(eVgo.head(), eVgo.tail(10))

eVgo['Adj Close'].plot()
plt.grid()
plt.show()

stationarityTest(eVgo)


# make a VAR model
model = VAR(eVgo)
resutlOrder = model.select_order(15)
print(resutlOrder.summary(), resutlOrder, **sp)
results = model.fit(maxlags=15, ic='aic')
lag_order = results.k_ar
print(lag_order)

results = model.fit(lag_order)

print(results.summary(), **sp)
with plt.style.context(style="ggplot"):
    results.plot()
    results.plot_acorr()
    plt.tight_layout()
    plt.show()

forcast5 = results.forecast(eVgo.values[-lag_order:], 20)
print(forcast5, **sp)

with plt.style.context(style="ggplot"):
    results.plot_forecast(10)
    plt.tight_layout()
    plt.show()

irf = results.irf(10)

with plt.style.context(style="ggplot"):
    irf.plot(orth=False)
    irf.plot_cum_effects(orth=False)
    plt.tight_layout()
    plt.show()
    
