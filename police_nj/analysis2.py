#!/usr/bin/env python
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict
import pickle
plt.style.use('ggplot')

path = "C:\\Users\\Jose\\Desktop\\TimerSeriesAnalysis\\police_nj\\"

os.chdir(path)

with open('clean_RI.pickle', 'rb') as f:
    # The protocol version used is detected automatically, so we do not
    # have to specify it.
    data = pickle.load(f)
    df = pd.DataFrame(data)

print(df.head())
print(df.shape)

print(df.isnull().sum())

print(df.is_arrested.value_counts(normalize=True))
print(df.dtypes)
print(df.is_arrested.mean())  # works only for boolean, True/False

# calculate the arrest rate by district and gender
print(df.groupby('district').is_arrested.mean())
print(df.groupby(['district', 'driver_gender']).is_arrested.mean())
print(df.groupby(['driver_gender', 'district']).is_arrested.mean())



# Calculate the search rate by counting the values
print(df.search_conducted.dtype)
print(df.search_conducted.value_counts(normalize=True))

# Calculate the search rate by taking the mean
print(df.search_conducted.mean())


# calculate the search rate by district and gender
df['search_conducted'] = df['search_conducted'].astype('bool')
print(df.groupby(['district', 'driver_gender']).search_conducted.mean())
print(df.groupby(['driver_gender', 'district']).search_conducted.mean())
print(df.groupby(['driver_gender', 'violation']).search_conducted.mean())