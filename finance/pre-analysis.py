import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import pickle

from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.decomposition import PCA
import bisect 

from datetime import datetime
from printdescribe import changepath

from datetime import datetime
startTime = datetime.now()

path1 = r"C:\Users\HP\Downloads"
path2 = r"C:\Users\HP\Documents\capstone"


with changepath(path1):
    data = pd.read_csv("spy_vix.csv")


# store a pickle and measure the time
# saving pickle
with changepath(path2):
    # %time pickle.dump(data, open("test.pkl","wb"))  ==> use only in jupyter notebook
    startTime = datetime.now()
    pickle.dump(data, open("test.pkl","wb"))
    print(datetime.now() - startTime)

    # Loading pickle
    startTime = datetime.now()
    # %time pickle.load(open("test.pkl","rb")) ==> use only in jupyter notebook
    pickle.load(open("test.pkl","rb"))
    print(datetime.now() - startTime)

with changepath(path2):
    startTime = datetime.now()
    # %time data.to_csv("spy_vix.csv") ==> use only in jupyter notebook
    data.to_csv("spy_vix.csv")
    print(datetime.now() - startTime)

    startTime = datetime.now()
    # %time pd.read_csv("spy_vix.csv") ==> use only in jupyter notebook
    pd.read_csv("spy_vix.csv")
    print(datetime.now() - startTime)

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
ddcol = [3, 6, 7, 8, 9, 10, 11, 12, 18,]
col = [dd[i] for i in ddcol]
df = data.loc[:,col]
df.head()

colname = 'DateTime OpenSPY HighSPY LowSPY LastSPY VolumeSPY CloseBidSPY CloseAskSPY VIX'.split()
df.columns = colname

# change to index
df['TimeIndex'] = df2['TimeIndex']
df.set_index("TimeIndex", inplace=True)
print(df.head())


# Graphical exploration I
plt.figure(figsize =(14,8))
plt.plot(df.loc[:,["OpenSPY", "VIX"]])
plt.grid(); plt.legend(["SPY Open", "VIX"])
plt.xticks(rotation=30)
plt.show()

# Graphical exploration II
df['deltaVIX'] = df.VIX.diff()
plt.figure(figsize =(14,8))
plt.plot(df.loc[:,["OpenSPY", "deltaVIX"]])
plt.grid(); plt.legend(["SPY Open", "VIX Differenced"])
plt.xticks(rotation=30)
plt.show()

# Graphical exploration III
fig, (ax1, ax2) = plt.subplots(2, sharex=True, figsize =(14,8))
ax1.grid(); ax2.grid()
ax1.set_title("SPY Open"); ax2.set_title("VIX Differenced")
ax1.plot(df.loc[:,["OpenSPY"]])
ax2.plot(df.loc[:,["deltaVIX"]])
plt.xticks(rotation=30)
plt.show()

# Graphical exploration IV
df['PerdeltaVIX'] = df.VIX.pct_change()
fig, (ax1, ax2) = plt.subplots(2, sharex=True, figsize =(14,8))
ax1.grid(); ax2.grid()
ax1.set_title("SPY Open"); ax2.set_title("VIX Percentage Change")
ax1.plot(df.loc[:,["OpenSPY"]])
ax2.plot(df.loc[:,["PerdeltaVIX"]])
plt.xticks(rotation=30)
plt.show()

# Explore feature engineering
df['Spread'] = df.CloseAskSPY - df.CloseBidSPY
df["HLDiff"] = df.HighSPY - df.LowSPY
f["deltaVolume"] = df.VolumeSPY.diff()
