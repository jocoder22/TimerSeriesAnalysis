#!/usr/bin/env python
import sys
from cmath import e
from typing import KeysView
import numpy as np
import pandas as np
import matplotlib.pyplot as plt

import statsmodels.api as sm
from statsmodels.tsa.api import VAR

import yfinance as yf

sys.path.append("E:\TimerSeriesAnalysis")

from stationarity.stationarity_conversion import stationarityTest


sp = {"sep":"\n\n", "end":"\n\n"}

#  load the dataset
eVgo = yf.download('EVGO')[["Adj Close", "Volume"]]

print(eVgo.head(), eVgo.tail(10), **sp)

eVgo['Adj Close'].plot()
plt.grid()
plt.show()

eVgo.iloc[-40:, 1].plot()
plt.grid()
plt.show()

stationarityTest(eVgo["Adj Close"])
eVgo_lag4 =  eVgo["Adj Close"].diff(periods=4).dropna()

print(f"#################     Testing 4 lagged dataset     ###################################")
stationarityTest(eVgo_lag4)

# make a VAR model
model = VAR(eVgo)
resutlOrder = model.select_order(15)
print(resutlOrder.summary(), resutlOrder, **sp)
results = model.fit(maxlags=15, ic='aic')
lag_order = results.k_ar
print(lag_order, **sp)

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
    
