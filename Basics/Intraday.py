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

pathtk = r"D:\PPP"
sys.path.insert(0, pathtk)

import wewebs

sp = {'sep': '\n\n', 'end': '\n\n'}
path = r"D:\Intradays"
ttt = wewebs.token

# aapl = Stock("AAPL", output_format='pandas', token=ttt)
# print(aapl.get_historical_prices())
# folders = ['S&P500','Dow30', 'Nasdaq', 'Russell2000', 'CrudeOil', 'Amazon', 'Apple', 'MicroSoft', 'Google']
# symbols = ['^GSPC', '^DJI', '^IXIC', '^RUT', 'CL=F', 'AMZN', 'AAPL', 'MSFT', 'GOOGL']

folders = ['Apple', 'MicroSoft', 'Google', 'Netflix', 'Tesla', 'Amazon', 'Toyota', 'JPMorgan', 'Citigroup']
symbols = ['AAPL', 'MSFT', 'GOOGL', 'NFLX', 'TSLA', 'AMZN', 'TM', 'JPM', 'C']

intradata = pd.DataFrame()
limitday = 61
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
    print(f'This is for {folders[idx]}', **sp)
    print(intradata.head(), intradata.columns, n, **sp)
    print(intradata.shape, intradata.info(), **sp)
