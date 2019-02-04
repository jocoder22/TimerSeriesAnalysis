#!/usr/bin/env python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import datasets
# plt.style.use('ggplot')
import pickle as pkl
from statsmodels.tsa.arima_process import ArmaProcess
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.arima_model import ARMA
from statsmodels.graphics.tsaplots import plot_pacf

from datetime import datetime

myTimeStamp =  pd.Timestamp(datetime(2018, 11, 9))

assert pd.Timestamp('2018-11-9') ==  myTimeStamp

print(myTimeStamp)
print(myTimeStamp.year, myTimeStamp.weekday_name)


myperiod = pd.Period('2019, 1')
print(myperiod)
myperiod.asfreq('D')
print(myperiod)

myperiod.to_timestamp().to_period('M')
print(myperiod)

print(myperiod + 2)

print(pd.Timestamp('2017-1-31', 'M') + 1)


index = pd.date_range(start='2018-1-1', periods=12, freq='M')
print(index)
print(index[0])

# index.to_period()
print(index.to_period()[:5])

df2 = pd.DataFrame({'Data': index})
print(df2.head())
data = np.random.random(size=[12, 2])
df = pd.DataFrame(data=data, index=df2['Data'])
print(df.head())



# Create the range of dates here
seven_days = pd.date_range(start='2017-1-1', periods=7)

# Iterate over the dates and print the number and name of the weekday
for day in seven_days:
    print(day.dayofweek, day.weekday_name)