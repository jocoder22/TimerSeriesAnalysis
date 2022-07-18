#!/usr/bin/env python
import os
import sys
import numpy as np
import pandas as pd

import  time
from datetime import timedelta, date

from iexfinance.stocks import Stock, get_historical_intraday, get_historical_data
from printdescribe import print2, changepath

pathtk = r"E:\PPP"
sys.path.insert(0, pathtk)

import wewebs

folders = wewebs.folders
symbols = wewebs.symbols

# folders = [ "Twilio","ExpWorld", "HomeDepot", 
# folders = ["Ford", "PVH", "Twitter", "Salesforce", "Alibaba", 
#             "NioElectricMotor", "Apple" ,  "BristolMyers", "XPeng",  "ChargingPoint", "GeneralElectric", 
#             "LiAuto", "Schrodinger", "Nvidia", "Marvel", "PaloAlto", "Proofprint", "Mandiant", "TenableHoldings"]
            
# symbols = ['TWLO', 'EXPI', 'HD',
# symbols = [ 'F', 'PVH', 'TWTR', 'CRM', 'BABA', 'NIO', 'AAPL', 'BMY', 'XPEV', 'CHPT', 'GE', 'LI', 
#               'SDGR', 'NVDA', 'MRVL', 'PANW', 'PFPT', 'MNDT', 'TENB']

# folders = ["XPeng", "ChargingPoint", "GeneralElectric", "LiAuto", "Schrodinger"]
# symbols = ['XPEV', 'CHPT', 'GE', 'LI', 'SDGR']

# print(folders)

# sp = {'sep': '\n\n', 'end': '\n\n'}
path = r"E:\Intradays"
# path1 = r"E:\Intradays\AdvancedMicroDevices"

ttt = wewebs.token
limitday = 90

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

# symbols = ['BABA', 'NIO', 'AAPL', 'BMY']
# folders = ["Alibaba", "NioElectricMotor", "Apple" ,  "BristolMyers"]

intradata = pd.DataFrame()
dattt = date.today()
datt2 = dattt.strftime("%d_%b_%Y")

for idx in range(len(symbols)):
    # os.chdir(path)
    # _dir = os.path.join(os.getcwd(), folders[idx])
    with changepath(path):
        _dir = os.path.join(os.getcwd(), folders[idx])

    if not os.path.isdir(_dir):
        os.makedirs(_dir)
        stdate = date.today() - timedelta(days=limitday)
    else:
        stdate = get_lastdate(_dir)

    intradata = pd.DataFrame()
    n = 0

    if date.today() ==  stdate:
        print2(f"Downloaded {folders[idx]} Data today")
        continue # continue with the next iteration i.e go to the top of the for loop

    while date.today() > stdate:
        startdate = stdate + timedelta(days=1)
        df2 = get_historical_intraday(symbols[idx], startdate, token=ttt, output_format='pandas')
        n += 1
        df2['Day'] = n
        df2.index.rename('Datetime', inplace=True)
        intradata = pd.concat([intradata, df2], axis=0, sort=True)
        stdate = startdate
        # startdate +=  timedelta(days=1)
        time.sleep(1.0) # seconds
    
    
    # saving our data
    # os.chdir(_dir)
    with changepath(_dir):
        intradata.to_csv(f'intraday_{datt2}.csv')
    print2(f'This is for {folders[idx]}')
    print2(intradata.head(), intradata.columns, n)
    print2(intradata.shape, intradata.info())

print("Done! TenableHoldings is the last!")

folders222 = ['Apple', 'MicroSoft', 'Google', 'Netflix', 'Tesla', 'Amazon', 'Toyota', 'JPMorgan', 
            'Citigroup', 'Walmat', 'Target', "Fedex", "Ups", "Walgreens", "Disney", "Pfizer",
            "Cvs", "AT_T", "CocaCola", "Boeing", "SolarEdge", "AdvancedMicroDevices", "Twilio",
            "ExpWorld", "HomeDepot", "Ford", "PVH", "Twitter", "Salesforce", 
            "Alibaba", "NioElectricMotor", "Apple" ,  "BristolMyers"]
symbols222 = ['AAPL', 'MSFT', 'GOOGL', 'NFLX', 'TSLA', 'AMZN', 'TM', 'JPM', 'C', 'WMT', 'TGT', 'FDX',
            'UPS', 'WBA', 'DIS', 'PFE', 'CVS', 'T', 'KO', 'BA', 'SEDG', 'AMD', 'TWLO', 'EXPI', 'HD',
              'F', 'PVH', 'TWTR', 'CRM', 'BABA', 'NIO', 'AAPL', 'BMY']


folders2 = ["ExtremeVehicleBattery", "SolarAllianceEnergy", "SponsorsOne", "iQSTEL"]
symbols2 = ["CRYBF", "SAENF", "SPONF", "IQST"]



gg = ["BABA", "AMD", "MSFT", "CRM", "BMY"]



