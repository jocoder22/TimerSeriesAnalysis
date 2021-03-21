import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.decomposition import PCA
import bisect 

from datetime import datetime
from printdescribe import changepath

path1 = r"C:\Users\HP\Downloads"

with changepath(path1):
    data = pd.read_csv("spy_vix.csv")

print(data.head())
print(data.iloc[:6,1:8])
print(data.iloc[:6,8:15])
print(data.iloc[:6,15:])

print(data.columns)
print(data.info())

dd = data.columns.tolist()
ddcol2 = [3, 6, 7, 8, 9, 10, 11, 12, 13, 18, 19, 20, 21]
col2 = [dd[i] for i in ddcol2]
df2 = data.loc[:,col2]
col22 = ['Date_Time', 'Open', 'High', 'Low', 'Last', 'Volume', 'Close_Bid',
       'Close_Ask', 'RIC.1', 'Open1', 'High1', 'Low1', 'Last1']
df2.columns = col22
df2.head()

# dealing with timestamp
# df2['from_timestamp']=data['Date_Time'].values.astype('datetime64[s]')
# df2['from_timestamp22'] = data['Date_Time'].apply(lambda t: datetime.fromisoformat(t[:-11]))
df2['TimeIndex']= data['Date_Time'].apply(lambda t:datetime.strptime(t[:-11], "%Y-%m-%dT%H:%M:%S"))
df2.info()

# checking if 'Open1', 'High1', 'Low1', 'Last1' are all equal
# so select any one of them
query = '''
        Open1 != High1 or Open1 != Low1 or  Open1 != Last1 or \
        Low1 != Last1 or Low1 != High1 or High1 != Last1
        '''

df2.query(query).shape