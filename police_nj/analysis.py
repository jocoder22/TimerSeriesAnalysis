#!/usr/bin/env python
import os 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('ggplot')


path = "C:\\Users\\Jose\\Desktop\\TimerSeriesAnalysis\\police_nj\\"
os.chdir(path)

wy = pd.read_csv('cleaned_wy.csv', parse_dates=True, index_col='stop_datetime')
print(wy.head())
print(wy.info())
