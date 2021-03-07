#!/usr/bin/env python
import os
import sys
import numpy as np
import pandas as pd

import datetime, time
from datetime import datetime, timedelta, date


from iexfinance.stocks import Stock, get_historical_intraday, get_historical_data
from printdescribe import print2

pathtk = r"E:\PPP"
sys.path.insert(0, pathtk)

import wewebs

sp = {'sep': '\n\n', 'end': '\n\n'}
path = r"E:\Intradays"
path1 = r"E:\Intradays\AdvancedMicroDevices"

ttt = wewebs.token
limitday = 80

def get_lastdate(path4):
    datelist = []
    dir_entries = os.scandir(path4)
    for entry in dir_entries:
        if entry.is_file():
            info = entry.stat()
            datelist.append(info.st_mtime)
            
    return date.fromtimestamp(max(datelist))


# folders = ["Schrodinger", "BristolMyers"]
# symbols = ['SDGR', 'BMY']

symbols = ['BABA', 'NIO', 'AAPL', 'BMY']
folders = ["Alibaba", "NioElectricMotor", "Apple" ,  "BristolMyers"]


intradata = pd.DataFrame()
dattt = date.today()
datt2 = dattt.strftime("%d_%b_%Y")



"""
folders = ['Apple', 'MicroSoft', 'Google', 'Netflix', 'Tesla', 'Amazon', 'Toyota', 'JPMorgan', 
            'Citigroup', 'Walmat', 'Target', "Fedex", "Ups", "Walgreens", "Disney", "Pfizer",
            "Cvs", "AT_T", "CocaCola", "Boeing", "SolarEdge", "AdvancedMicroDevices", "Twilio",
            "ExpWorld", "HomeDepot", "Ford", "PVH", "Twitter", "Salesforce"]
symbols = ['AAPL', 'MSFT', 'GOOGL', 'NFLX', 'TSLA', 'AMZN', 'TM', 'JPM', 'C', 'WMT', 'TGT', 'FDX',
            'UPS', 'WBA', 'DIS', 'PFE', 'CVS', 'T', 'KO', 'BA', 'SEDG', 'AMD', 'TWLO', 'EXPI', 'HD',
              'F', 'PVH', 'TWTR', 'CRM']
"""
# os.chdir(path)
# for idx in range(len(symbols)):
#     _dir = os.path.join(os.getcwd(), folders[idx])
#     print2(_dir)
#     print2(get_lastdate(_dir))


for idx in range(len(symbols)):
    os.chdir(path)
    _dir = os.path.join(os.getcwd(), folders[idx])

    # savedir = os.path.join(os.getcwd(), folders[idx])
    if not os.path.isdir(_dir):
        os.makedirs(_dir)
        stdate = date.today() - timedelta(days=limitday)
    else:
        stdate = get_lastdate(_dir)

    # os.chdir(path)
    intradata = pd.DataFrame()
    n = 0

    if date.today() ==  stdate:
        print2(f"Downloaded {folders[idx]} Data today");
        continue
    

    while date.today() > stdate:
        startdate = stdate + timedelta(days=1)
        df2 = get_historical_intraday(symbols[idx], startdate, token=ttt, output_format='pandas')
        n += 1
        df2['Day'] = n
        df2.index.rename('Datetime', inplace=True)
        intradata = pd.concat([intradata, df2], axis=0, sort=True)
        stdate = startdate
        # startdate +=  timedelta(days=1)
        time.sleep(1.8) # seconds
        
    # saving data
    # savedir = os.path.join(os.getcwd(), folders[idx])
    # if not os.path.isdir(_dir):
    #     os.makedirs(_dir)
    os.chdir(_dir)
    intradata.to_csv(f'intraday_{datt2}.csv')
    print2(f'This is for {folders[idx]}')
    print2(intradata.head(), intradata.columns, n)
    print2(intradata.shape, intradata.info())


