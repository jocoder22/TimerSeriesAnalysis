#!/usr/bin/env python
import pandas as pd
import yfinance as yf

from printdescribe import changepath

datapath = r"E:\TimerSeriesAnalysis\QuantitativeRiskManagement\Data"

Assets = 'CitiGroup MorganStanley GoldmanSachs JPMorgan'.split()
tickers = 'C MS GS JPM'

# Download the data
startdate = "2005-01-01"
enddate = "2010-12-31"

print("[getData] Downloading data ...")
stockdata = yf.download(tickers, start=startdate, end=enddate)[['Adj Close']].droplevel(0, axis=1)
stockdata.columns = Assets

with changepath(datapath):
    stockdata.to_csv(f"assetsData.csv")

print("[getData] Done Downloading data!")