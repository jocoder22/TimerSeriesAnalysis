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


from iexfinance.stocks import get_historical_intraday, get_historical_data


sp = '\n\n'
path = r'C:\Users\Jose\Documents\Intradays'
os.chdir(path)

folders = ['S&P500','Dow30', 'Nasdaq', 'Russell2000', 'CrudeOil', 'Amazon', 'Apple', 'MicroSoft', 'Google']
symbols = ['^GSPC', '^DJI', '^IXIC', '^RUT', 'CL=F', 'AMZN', 'AAPL', 'MSFT', 'GOOGL']


intradata = pd.DataFrame()
limitday = 90
stdate = date.today() - timedelta(days=limitday)


dattt = date.today()
datt2 = dattt.strftime("%d_%b_%Y")
print(date.today() > stdate)
for idx in range(len(symbols)):
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
    intradata.to_csv(f'intraday_{datt2}.csv')
    print(intradata.head(), intradata.columns, n,  sep=sp)
    print(intradata.shape, intradata.info(), sep=sp)



