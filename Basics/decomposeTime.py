#!/usr/bin/env python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader as pdr
import yfinance as yf
from datetime import datetime, date

startdate = datetime(2010,11,1)
enddate = datetime(2019,1,30)


allstocks = ["^VIX", "SPY"]
allstocks = "^VIX SPY"
ticker = "BABA"

allstocks = pdr.get_data_yahoo(ticker, startdate).reset_index()
allstocks['year'] = allstocks["Date"].apply(lambda x: str(x.isocalendar()[0]))
allstocks['weekNumb'] = allstocks["Date"].apply(lambda x: str(x.isocalendar()[1]))
allstocks['weekday'] = allstocks["Date"].apply(lambda x: str(x.isocalendar()[2]))
print(allstocks.head())
# print(date(2010, 6, 16).isocalendar()[2])
# print(date.today().isocalendar())

weekdaymean = allstocks.groupby("weekNumb").agg({"Adj Close":"min"}).sort_values("Adj Close", ascending=False)

weekdaymean.plot(kind="bar")
plt.show()