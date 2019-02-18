#!/usr/bin/env python
import os
import io
import gzip
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests
from collections import defaultdict
import pickle
plt.style.use('ggplot')


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


path = "C:\\Users\\Jose\\Desktop\\TimerSeriesAnalysis\\police_nj\\"

os.chdir(path)

url = 'https://stacks.stanford.edu/file/druid:py883nd2578/RI-clean.csv.gz'

r = requests.get(url, stream=True)

rfile = io.BytesIO(r.content); 
tts = []

with gzip.GzipFile(fileobj=rfile) as gzfile:
    for chunk in pd.read_csv(gzfile, chunksize=100000, low_memory=False):
        tts.append(chunk)

df = pd.concat(tts)

df['is_arrested'] = df['is_arrested'].astype('bool')
print(df.info())
print(df.head())        
find_per_missing(df)
find_unique(df)


df.replace(to_replace=['NA:NA', '24:00'], value=[np.nan,'23:59'], inplace=True)
df.stop_time.interpolate(method='linear', limit_direction='forward', axis=0, inplace=True)
df.stop_date.interpolate(method='pad', inplace=True)
df.dropna(subset=['stop_time'], inplace=True)
fulltime = df.stop_date.str.cat(df.stop_time, sep=' ')

# Convert 'combined' to datetime format
df['fulldatetime'] = pd.to_datetime(fulltime)

# set index with stop_datetime
df.set_index('fulldatetime', inplace=True)
df.index.rename('stop_datetime', inplace=True)

# drop using index column
# df.dropna(subset=df.index.name, inplace=True)
df.drop(list(df.columns[0:9]), axis=1, inplace=True)
df.drop(['search_type_raw', 'search_type', 'driver_age_raw', 'driver_race_raw'], 
        axis=1, inplace=True)

print(df.info())
print(df.head())
print(df.tail())

# df.to_csv('clean_RI.csv')  ### file here is very large
# save file as pickled file to save space
with open('clean_RI.pickle', 'wb') as f:
    # Pickle the 'data' dictionary using the highest protocol available.
    pickle.dump(df, f, pickle.HIGHEST_PROTOCOL)