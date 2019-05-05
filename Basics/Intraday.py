#!/usr/bin/env python
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

from iexfinance.stocks import get_historical_intraday, get_historical_data


sp = '\n\n'
path = r'C:\Users\Jose\Documents\Intradays'


# folders = ['S&P500','Dow30', 'Nasdaq', 'Russell2000', 'CrudeOil', 'Amazon', 'Apple', 'MicroSoft', 'Google']
# symbols = ['^GSPC', '^DJI', '^IXIC', '^RUT', 'CL=F', 'AMZN', 'AAPL', 'MSFT', 'GOOGL']

folders = ['Apple', 'MicroSoft', 'Google', 'Netflix', 'Tesla', 'Amazon']
symbols = ['AAPL', 'MSFT', 'GOOGL', 'NFLX', 'TSLA', 'AMZN']

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
        df2 = get_historical_intraday(symbols[idx], startdate, output_format='pandas')
        n += 1
        df2['Day'] = n
        df2.index.rename('Datetime', inplace=True)
        intradata = pd.concat([intradata, df2], axis=0)
        stdate = startdate
        time.sleep(0.8) # seconds
    # saving data
    savedir = os.path.join(os.getcwd(), folders[idx])
    if not os.path.isdir(savedir):
        os.makedirs(savedir)
    os.chdir(savedir)
    intradata.to_csv(f'intraday_{datt2}.csv')
    print(intradata.head(), intradata.columns, n,  sep=sp, end=sp)
    print(intradata.shape, intradata.info(), sep=sp)



