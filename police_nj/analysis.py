#!/usr/bin/env python
import os 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import gzip, requests


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
"""
wy = pd.read_csv('Data-wy.csv')
print(wy.head())

print(wy.shape)