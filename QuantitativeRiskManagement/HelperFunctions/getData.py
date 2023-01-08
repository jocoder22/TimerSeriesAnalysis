#!/usr/bin/env python
import pandas as pd
import yfinance as yf

import pandas_datareader.data as web
import datetime

from printdescribe import changepath

datapath = r"E:\TimerSeriesAnalysis\QuantitativeRiskManagement\Data"

Assets = 'CitiGroup GoldmanSachs JPMorgan MorganStanley '.split()
tickers = 'C MS GS JPM'

# Download the data
startdate = "2005-01-01"
enddate = "2010-12-31"

print("[getData] Downloading data ...")

stockdata = yf.download(tickers, start=startdate, end=enddate)[['Adj Close']].droplevel(0, axis=1)
stockdata.columns = Assets

stockdata2 = yf.download(tickers, start=startdate, end=enddate)[['Close']].droplevel(0, axis=1)
# print(stockdata2.columns)
stockdata2.columns = Assets

mort_del_rate_fred = web.DataReader('DRSFRMACBS', 'fred', startdate, enddate)
mort_30rate_fred = web.DataReader('MORTGAGE30US', 'fred', startdate, enddate)
mort__Income_fred = web.DataReader('MDSP', 'fred', startdate, enddate)

weblink = "https://s3.amazonaws.com/files.consumerfinance.gov/data/mortgage-performance/downloads/CountyMortgagesPercent-90-plusDaysLate-thru-2022-06.csv"
weblink2 = "https://s3.amazonaws.com/files.consumerfinance.gov/data/mortgage-performance/downloads/CountyMortgagesPercent-30-89DaysLate-thru-2022-06.csv"

mort_del_rate_cusFin = pd.read_csv(weblink)
mort_del_rate_cusFin2 = pd.read_csv(weblink2)

with changepath(datapath):
    stockdata.to_csv(f"assetsData.csv")
    stockdata2.to_csv(f"assetsDataClose.csv")
    mort_del_rate_cusFin.to_csv('mort_del_R90+_cf.csv')
    mort_del_rate_cusFin2.to_csv('mort_del_R3090_cf.csv')
    mort_del_rate_fred.to_csv('mort_del_R_fred.csv')
    mort_30rate_fred.to_csv('mort_30rate_R_fred.csv')
    mort__Income_fred.to_csv('mort_income_fred.csv')

print("[getData] Done Downloading data!")