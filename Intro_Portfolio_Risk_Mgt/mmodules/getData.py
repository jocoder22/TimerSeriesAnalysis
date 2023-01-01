#!/usr/bin/env python
import pandas as pd
import yfinance as yf

from printdescribe import changepath

datapath = r"E:\TimerSeriesAnalysis\Intro_Portfolio_Risk_Mgt\Data"

Assets = '''Apple Miscrosoft ExxonMobil Johnson&Johnson JPMorgan Amazon
         GeneralElectric Facebook AT&T S&P500'''.split()
tickers = 'AAPL MSFT XOM JNJ JPM AMZN GE META T ^GSPC'

sp = {"end":"\n\n", "sep":"\n\n"}

# Download the data
startdate = "2010-01-01"
enddate = "2022-12-31"

print("[getData] Downloading data ...")
stockdata = yf.download(tickers, start=startdate, end=enddate)[['Adj Close']].droplevel(0, axis=1)
stockdata.columns = Assets
print("[getData] Done Downloading data!")


with changepath(datapath):
    print("[getData] Start saving data ...")
    stockdata.to_csv("portfolio2.csv", index=True)
    print("[getData] Done saving data!")




