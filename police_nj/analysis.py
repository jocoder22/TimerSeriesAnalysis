#!/usr/bin/env python
import os 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import gzip, requests
from datetime import datetime
from collections import defaultdict


print(os.getcwd())

path = "C:\\Users\\Jose\\Desktop\\TimerSeriesAnalysis\\police_nj\\"
os.chdir(path)

""" 
url = 'https://stacks.stanford.edu/file/druid:py883nd2578/WY-clean.csv.gz'

# Download, read, and form dataframe
filename = url.split('/')[-1]
with open(filename, "wb") as f:
    r = requests.get(url)
    f.write(r.content)
    with gzip.open(filename, 'rb') as gzfile:
        wy = pd.read_csv(gzfile)
        wy.to_csv('Data-wy.csv', index=False)

headers = ['col1', 'col2', 'col3', 'col4']
dtypes = {'col1': 'str', 'col2': 'str', 'col3': 'str', 'col4': 'float'}
parse_dates = ['col1', 'col2']
pd.read_csv(file, sep='\t', header=None, names=headers, dtype=dtypes, parse_dates=parse_dates
time_format = '%Y-%m-%d %H:%M'
"""
""" wy = pd.read_csv('Data-wy.csv') 
# wy2 = pd.read_csv('Data-wy2.csv', na_values=["NA:NA", " NA:NA"]) 


# wy.rename({"stop_date_stop_time":"date"}, axis='columns', inplace=True)
# wy.index.rename('Date', inplace=True)
# wy.index = wy.index.astype('datetime64')


# print(wy2.info())
# print(wy2.isnull().sum())
# print(wy2.head())
# # wy.drop(subset=['stop_time'])
# wy2.replace(to_replace ='24:00', value='23:59', inplace=True)
# data["Age"]= data["Age"].replace(25.0, "Twenty five")
 

wy.replace(to_replace =['NA:NA', '24:00'], value=[np.nan,'23:59'], inplace=True)
wy.dropna(subset=['stop_time', 'stop_date'], inplace=True)
wy.to_csv('Data-wy2.csv', index=False)"""

wy2 = pd.read_csv('Data-wy2.csv', parse_dates={'date':['stop_date', 'stop_time']})
time_format = '%Y-%m-%d %H:%M'
wy2['date'] = pd.to_datetime(wy2.date, format=time_format) 
print(wy2.info())

print(wy2.head())


""" print(wy.dtypes)
print(wy.info())
print(wy.head())
print(wy.shape)



ddd = dict(wy.isnull().sum())
dd = defaultdict(list)
nn = wy.shape[0]
for key, value in ddd.items():
    dd['name'].append(key)
    dd['missing'].append(value)
    if value == 0:
        dd['%_missing'].append(value)
    else:
        val = 100 * value / nn 
        dd['%_missing'].append(f'{val:.2f}')

mm = pd.DataFrame(dd)
print(mm)

wy.drop(list(wy.columns[16:22]), axis=1, inplace=True)
print(wy.columns) """