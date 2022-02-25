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

allstocks = pdr.get_data_yahoo(ticker, startdate)[["Adj Close"]].reset_index()
allstocks['year'] = allstocks["Date"].apply(lambda x: str(x.isocalendar()[0]))
allstocks['quarter'] = allstocks["Date"].apply(lambda x: str(x.quarter))
allstocks['weekNumb'] = allstocks["Date"].apply(lambda x: str(x.isocalendar()[1]))
allstocks['weekday'] = allstocks["Date"].apply(lambda x: str(x.isocalendar()[2]))
allstocks['monthday'] = allstocks["Date"].apply(lambda x: x.strftime("%b%d"))
allstocks['month'] = allstocks["Date"].apply(lambda x: x.strftime("%b"))
allstocks['day'] = allstocks["Date"].apply(lambda x: x.strftime("%d"))


print(allstocks.head())


# # print(date(2010, 6, 16).isocalendar()[2])
# # print(date.today().isocalendar())

weekdaymean = allstocks.groupby("day").agg({"Adj Close":"max"}).sort_values("Adj Close", ascending=False)

weekdaymean.plot(kind="bar")
plt.show()

print(startdate.strftime("%b"))