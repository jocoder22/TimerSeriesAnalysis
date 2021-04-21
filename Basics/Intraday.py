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

pathtk = r"E:\PPP"
path = r"E:\Intradays"
sys.path.insert(0, pathtk)

import wewebs

sp = {'sep': '\n\n', 'end': '\n\n'}
# path = r"D:\Intradays"
# path = r"E:\Intradays"
# path = r"C:\Users\HP\Documents\intraday"

ttt = wewebs.token
folder = wewebs.folders
symbols = wewebs.symbols

# https://iexcloud.io/cloud-login#/

# Site for stoch symbols
#  https://iextrading.com/trading/eligible-symbols/
# aapl = Stock("AAPL", output_format='pandas', token=ttt)
# print(aapl.get_historical_prices())
# folders = ['S&P500','Dow30', 'Nasdaq', 'Russell2000', 'CrudeOil']
# symbols = [ '^RUT', 'CL=F', '^GSPC', '^DJI', '^IXIC']
# folders = ["Ford", "PVH", "Twitter", "Salesforce"]
# symbols = [ 'F', 'PVH', 'TWTR', 'CRM']

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



https://wqu-capstone.slack.com/archives/G01NSUR38GP/p1618798234058700

https://wqu-capstone.slack.com/archives/G01NSUR38GP/p1618798234058700


https://docs.google.com/document/d/1M82damLQQ5QnMVEfHeP4x-qqn2ODIdY-stbmqMvB3R8/edit#heading=h.gjdgxs