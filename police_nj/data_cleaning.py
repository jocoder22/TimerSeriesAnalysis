#!/usr/bin/env python
import os 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import gzip, requests
from datetime import datetime
from collections import defaultdict

def find_per_missing(dataframe):
    ddd = dict(dataframe.isnull().sum())
    dd = defaultdict(list)
    nn = dataframe.shape[0]
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

def find_unique(dataframe):
    dd2 = defaultdict(list)
    for item in list(dataframe.columns):
        dd2['name'].append(item)
        dd2['dtype'].append(dataframe[item].dtype)
        unique = len(dataframe[item].unique())
        dd2['number_unique'].append(unique)

    mm2 =  pd.DataFrame(dd2)
    print(mm2)


print(os.getcwd())

path = "C:\\Users\\Jose\\Desktop\\TimerSeriesAnalysis\\police_nj\\"
os.chdir(path)


url = 'https://stacks.stanford.edu/file/druid:py883nd2578/WY-clean.csv.gz'

# Download, read, and form dataframe
filename = url.split('/')[-1]
with open(filename, "wb") as f:
    r = requests.get(url)
    f.write(r.content)
    with gzip.open(filename, 'rb') as gzfile:
        wy = pd.read_csv(gzfile)
        wy.to_csv('Data-wy.csv', index=False)


find_per_missing(wy)
print(wy.head())
print(wy.info())
print(wy.isnull().sum())
print(wy.columns)

# drop id, state and county columns
wy.drop(['id', 'state', 'county_name'], axis='columns', inplace=True)
find_per_missing(wy)

# remove columns with 100% missing
wy.drop(list(wy.columns[13:19]), axis=1, inplace=True)
find_per_missing(wy)

# drop row with missing driver's gender
# Drop all rows that are missing 'driver_gender'
wy.dropna(subset=['driver_gender'], inplace=True)


# find number of unique values per column, driver's gender has 2
# unique values, M and F;  so will be good features for categorical data type
find_unique(wy)

wy['driver_gender'] = wy.driver_gender.astype('category')

find_unique(wy)
print(wy['driver_gender'].unique())

wy.replace(to_replace =['NA:NA', '24:00'], value=[np.nan,'23:59'], inplace=True)
wy.stop_time.interpolate(method='linear', limit_direction='forward', axis=0, inplace=True)
wy.stop_date.interpolate(method='pad', inplace=True)
fulltime = wy.stop_date.str.cat(wy.stop_time, sep=' ')

# Convert 'combined' to datetime format
wy['fulldatetime'] = pd.to_datetime(fulltime)

# set index with stop_datetime
wy.set_index('fulldatetime', inplace=True)

wy.index.rename('stop_datetime', inplace=True)
wy.drop(['stop_date', 'stop_time'], axis='columns', inplace=True)
# Examine the data types of the DataFrame
print(wy[['violation', 'driver_age']].tail())
print(wy.tail())

wy.to_csv('cleaned_wy.csv', index=False)



wy2 = pd.read_csv('Data-wy2.csv', parse_dates={'date':['stop_date', 'stop_time']})
time_format = '%Y-%m-%d %H:%M'
wy2['date'] = pd.to_datetime(wy2.date, format=time_format) 
print(wy2.info())

print(wy2.head())




