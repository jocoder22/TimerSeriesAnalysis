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
# Today's date and time
today1 = datetime.now()  # give to nanoseconds:  2019-03-17 17:44:21.574530
today2 = date.today()  # give only the day: 2019-03-17
print(today1, today2, sep=sp) 

# # Creating date
# tomorrow = date(2019, 4, 18)

# print(tomorrow)

# # Get date form timestamp: number of second between date and january 1, 1970 in UTC
# # convert tiemstamp to date using fromtimestamp()
# timestamp = date.fromtimestamp(1554611045)
# print("Date =", timestamp)

# # working with datetime (year, month, day, hour, minutes, seconds, nanosecods)
# mydate = datetime(2019, 12, 24, 18, 51, 58, 380342)
# print("year =", mydate.year)
# print("month =", mydate.month)
# print("hour =", mydate.hour)
# print("minute =", mydate.minute)
# print("timestamp =", mydate.timestamp(), end=sp)

# # mainpulating date
# # with timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)
# maydate = date(2018, 5, 15)
# print(maydate, maydate + timedelta(days=1), date.today() - maydate, maydate.weekday(), sep=sp)
# print(type(date.today() - maydate))
# # date.weekday(): Monday is 0 and Sunday is 6
# print(maydate.weekday(), end=sp)
# # date.isoweekday() : Monday is 1 and Sunday is 7
# print(maydate.isoweekday(), end=sp)

# # get the intraday stock for last 90 days
# date = datetime(2018, 11, 27)

# stocksname ='AAL'
# startdate = datetime(2014, 1, 1)
# enddate = datetime(2019, 3, 16)
# df = get_historical_data(stocksname, startdate, enddate, output_format='pandas')
# print(df.shape)

n = 0
intradata = pd.DataFrame()
limitday = 91
stdate = date.today() - timedelta(days=limitday)
print(stdate)

path = r'C:\Users\Jose\Documents\Intradays'
os.chdir(path)

dattt = date.today()
datt2 = dattt.strftime("%d_%b_%Y")
print(date.today() > stdate)
while date.today() > stdate:
    startdate = stdate + timedelta(days=1)
    df2 = get_historical_intraday(stocksname, startdate, output_format='pandas')
    n += 1
    df2['Day'] = n
    # df2.index.set_names('Datetime', inplace=True)
    df2.index.rename('Datetime', inplace=True)
    intradata = pd.concat([intradata, df2], axis=0)
    stdate = startdate
intradata.to_csv(f'intraday_{datt2}.csv')
print(intradata.head(), intradata.columns, n,  sep=sp)
print(intradata.shape, intradata.info(), sep=sp)

# tday = date.today()
# print(tday.strftime("%A %d. %B %Y"))
# print(tday.strftime("%y %m %d"))
# print(tday.strftime("%Y %m %d"))
# tp = tday.timetuple()
# ic = tday.isocalendar()
# print(tp, ic, sep=sp, end=sp)
# for idx, item in enumerate(tp):
#     print(idx, item)
