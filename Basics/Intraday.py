#!/usr/bin/env python
import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('ggplot')

import datetime
from datetime import date
from datetime import datetime
from datetime import timedelta
import time

from iexfinance.stocks import Stock, get_historical_intraday, get_historical_data
from printdescribe import print2

pathtk = r"D:\PPP"
sys.path.insert(0, pathtk)

import wewebs

sp = {'sep': '\n\n', 'end': '\n\n'}
# path = r"D:\Intradays"
path = r"D:\Intradays"
# path = r"C:\Users\HP\Documents\intraday"
ttt = wewebs.token

# https://iexcloud.io/cloud-login#/

# Site for stoch symbols
#  https://iextrading.com/trading/eligible-symbols/
# aapl = Stock("AAPL", output_format='pandas', token=ttt)
# print(aapl.get_historical_prices())
# folders = ['S&P500','Dow30', 'Nasdaq', 'Russell2000', 'CrudeOil']
# symbols = [ '^RUT', 'CL=F', '^GSPC', '^DJI', '^IXIC']

# **
# folders = ['Apple', 'MicroSoft', 'Google', 'Netflix', 'Tesla', 'Amazon', 'Toyota', 'JPMorgan', 
#             'Citigroup', 'Walmat', 'Target', "Fedex", "Ups", "Walgreens", "Disney", "Pfizer",
#             "Cvs", "AT_T", "CocaCola", "Boeing", "SolarEdge", "AdvancedMicroDevices", "Twilio",
#             "ExpWorld", "HomeDepot", "Ford", "PVH", "Twitter", "Salesforce"]
# symbols = ['AAPL', 'MSFT', 'GOOGL', 'NFLX', 'TSLA', 'AMZN', 'TM', 'JPM', 'C', 'WMT', 'TGT', 'FDX',
#             'UPS', 'WBA', 'DIS', 'PFE', 'CVS', 'T', 'KO', 'BA', 'SEDG', 'AMD', 'TWLO', 'EXPI', 'HD',
#               'F', 'PVH', 'TWTR', 'CRM']
# **
# # 

folders = ["Ford", "PVH", "Twitter", "Salesforce"]
symbols = [ 'F', 'PVH', 'TWTR', 'CRM']


intradata = pd.DataFrame()
limitday = 80
dattt = date.today()
datt2 = dattt.strftime("%d_%b_%Y")

for idx in range(len(symbols)):
    stdate = date.today() - timedelta(days=limitday)
    os.chdir(path)
    intradata = pd.DataFrame()
    n = 0
    while date.today() > stdate:
        startdate = stdate + timedelta(days=1)
        df2 = get_historical_intraday(symbols[idx], startdate, token=ttt, output_format='pandas')
        n += 1
        df2['Day'] = n
        df2.index.rename('Datetime', inplace=True)
        intradata = pd.concat([intradata, df2], axis=0, sort=True)
        stdate = startdate
        time.sleep(1.8) # seconds
        
    # saving data
    savedir = os.path.join(os.getcwd(), folders[idx])
    if not os.path.isdir(savedir):
        os.makedirs(savedir)
    os.chdir(savedir)
    intradata.to_csv(f'intraday_{datt2}.csv')
    print2(f'This is for {folders[idx]}')
    print2(intradata.head(), intradata.columns, n)
    print2(intradata.shape, intradata.info())
