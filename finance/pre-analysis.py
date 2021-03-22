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

"""

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

"""

with changepath(path2):
    # Loading picklek
    data = pickle.load(open("test.pkl","rb"))
    

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


# Graphical exploration V
fig, ax1 = plt.subplots(figsize=[14,10])

color = 'tab:red'
ax1.set_xlabel('time (s)')
ax1.set_ylabel('SPY Open', color=color)
ax1.plot(df.OpenSPY, color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:blue'
ax2.set_ylabel('CBOE VIX', color=color)  # we already handled the x-label with ax1
ax2.plot(df.VIX, color=color)
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.show()


# Explore feature engineering
df['Spread'] = df.CloseAskSPY - df.CloseBidSPY
df["HLDiff"] = df.HighSPY - df.LowSPY
df["deltaVolume"] = df.VolumeSPY.diff()

# scale or normalized the data
# using minmax scaler
minmaxscaler = MinMaxScaler()
mmscaled = minmaxscaler.fit_transform(df.drop(columns = "DateTime"))
df_n = pd.DataFrame(mmscaled, columns = df.columns[1:])

print(df_n.corr())

## using standardized scaler
ssscaler = StandardScaler()
ssscaled = ssscaler.fit_transform(df.drop(columns = "DateTime" ))
df_n2 = pd.DataFrame(ssscaled, columns = df.columns[1:])


#### here the covariance and correlation are the same
print(df_n2.corr())
print(df_n2.cov())


# Doing Principal component analysis
X = df_n2.copy()
X = X.iloc[:,4:].dropna() # dropping spy prices
pca = PCA()
pca.fit_transform(X)
pce = pca.explained_variance_ratio_
print(pce.cumsum())


# find the number of components for greater than 96%
pcelist = pce.cumsum()
res = list(map(lambda i: i> 0.96, pcelist)).index(True)
print(res)


# re calcuate pca with estimate number of components
pca = PCA(n_components=res)
pca.fit_transform(X)
colname = ["PC"+ str(i) for i in range(1,res+1)]
loadings = pd.DataFrame(np.abs(pca.components_.T), columns=colname, 
                        index = X.columns)

print(loadings.sort_values(by="PC6", ascending=False))




# Here, we have 3 figures together
fig, ax1 = plt.subplots(figsize=[14,10])

color = 'tab:red'
ax1.set_xlabel('time (s)')
ax1.set_ylabel('Amazon', color=color)
ax1.plot(allstocks.loc[:,["AMZN", "GOOG"]])
ax1.tick_params(axis='y', labelcolor=color)
colormap = plt.cm.gist_ncar #nipy_spectral, Set1,Paired  
colors = ["red", "green"]

# colors = [colormap(i) for i in np.linspace(0, 1,len(ax1.lines))]
for i,j in enumerate(ax1.lines):
    j.set_color(colors[i])

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'black'
ax2.set_ylabel('Bank Of America', color=color)  # we already handled the x-label with ax1
ax2.plot(allstocks.BAC, color=color)
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.show()



from itertools import combinations
comb = combinations(allstocks.columns ,2)
print(len(list(comb)))

comb = combinations(allstocks.columns ,2)
for i in comb:
    fig, ax1 = plt.subplots(figsize=[14,10])

    color = 'tab:red'
    ax1.set_xlabel('time (s)')
    ax1.set_ylabel(f'{i[0]}', color=color)
    ax1.plot(allstocks[i[0]], color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    ax2.set_ylabel(f'{i[1]}', color=color)  # we already handled the x-label with ax1
    ax2.plot(allstocks[i[1]], color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped

    plt.show()
    print(end = "\n\n" * 4)
    
    
#   http://article.sciencepublishinggroup.com/html/10.11648.j.sjams.20150304.13.html#paper-content-2
# https://towardsdatascience.com/predict-time-stamped-sales-in-python-1914292461ad
