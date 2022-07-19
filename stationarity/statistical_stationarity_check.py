# https://www.analyticsvidhya.com/blog/2018/09/non-stationary-time-series-python/
#!/usr/bin/env python
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import yfinance as yf

from statsmodels.tsa.stattools import adfuller, kpss
import warnings
warnings.filterwarnings('ignore')


def adftest(timeseries):
    # Perform Dickey-Fuller test:
    print ('Results of Dickey-Fuller Test:')
    dftest = adfuller(timeseries, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','Number of Lags Used','Number of Observations Used'])
    for key,value in dftest[4].items():
       dfoutput[f'Critical Value {key}'] = value
    print (dfoutput)
    if dfoutput["Test Statistic"] > dfoutput["Critical Value 5%"]:
        print(f"The TimeSeries is not Stationary, p-value = {round(dfoutput['p-value'], 2)}", end="\n\n")
    else: print(f"The TimeSeries is Stationary, p-value = {round(dfoutput['p-value'], 2)}", end="\n\n")
   


def kpsstest(timeseries, **kw):
    # Perform Dickey-Fuller test:
    print ('Kwiatkowski-Phillips-Schmidt-Shin (KPSS) Test:')
    kpsstest = kpss(timeseries, nlags='auto', **kw)
    kpssoutput = pd.DataFrame({"Results": kpsstest[0:3]}, index=['Test Statistic','p-value','Number of Lags Used'])
    for key,value in kpsstest[3].items():
       kpssoutput.loc[f'Critical Value {key}', :] = value
    print (kpssoutput)
    if kpssoutput.loc["Test Statistic", :].values > kpssoutput.loc["Critical Value 5%", :].values:
        print(f"The TimeSeries is not Stationary, p-value = {round(kpssoutput.loc['p-value', :].values[0], 2)}")
    else: print(f"The TimeSeries is Stationary, p-value = {round(kpssoutput.loc['p-value', :].values[0], 2)}")
    print(f'Result: The TimeSeries is {"not " if kpssoutput.loc["p-value", :].values < 0.05 else ""}stationary', end="\n\n")


sp = {"sep":"\n\n", "end":"\n\n"}
airpassengers = "E:\TimerSeriesAnalysis\datasets\AirPassengers.csv"

# load the dataset
aapl = yf.download('AAPL', '2017-1-1','2022-6-30')[['Adj Close']]
train = pd.read_csv(airpassengers)
print(train.head(), aapl.head(), **sp)


adftest(train['#Passengers'])
adftest(aapl)

kpsstest(train['#Passengers'])
kpsstest(aapl)


# A major difference between KPSS and ADF tests is the capability of the KPSS test 
# to check for stationarity in the ‘presence of a deterministic trend’.
# also their Hull hypothesis are opposite

# What that effectively means to us is, the test may not necessarily reject the null hypothesis
#  (that the series is stationary) even if a series is steadily increasing or decreasing.

# The word ‘deterministic’ implies the slope of the trend in the series does not change permanently. 
# That is, even if the series goes through a shock, it tends to regain its original path.

kpsstest(train['#Passengers'], regression='ct')
kpsstest(aapl, regression='ct')

# So overall what this means to us is, if a series is stationary according to the KPSS test by 
# setting regression='ct' and is not stationary according to the ADF test, it means the series 
# is stationary around a deterministic trend and so is fairly easy to model this series and 
# produce fairly accurate forecasts.

# So in summary, the ADF test has an alternate hypothesis of linear or difference stationary,
#  while the KPSS test identifies trend-stationarity in a series.
