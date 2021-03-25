import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader as pdr

from datetime import datetime
# startdate = datetime(2010,11,1)
# enddate = datetime(2019,1,30)
startdate = datetime(2019, 1, 1)
# enddate = datetime(2020, 12, 31)

# statsmodels.tsa.stattools.bds(x, max_dim=2, epsilon=None, distance=1.5)[source]
from statsmodels.tsa.stattools import bds

allstocks = ["^VIX", "SPY"]

# allstocks = pdr.get_data_yahoo(allstocks, startdate, enddate)['Adj Close']
allstocks = pdr.get_data_yahoo(allstocks, startdate)['Adj Close']
print(allstocks.head())

allstocks.columns = ["OpenSPY", "VIX"]
allstocks.head()


df = allstocks.copy()

# Graphical exploration V
fig, ax1 = plt.subplots(figsize=[14,10])

color = 'tab:blue'
ax1.set_xlabel('time (s)')
ax1.set_ylabel('SPY Open', color=color)
ax1.plot(df.OpenSPY, color=color)
ax1.tick_params(axis='y', labelcolor=color)
ax1.grid()
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:red'
ax2.set_ylabel('CBOE VIX', color=color)  # we already handled the x-label with ax1
ax2.plot(df.VIX, color=color)
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.show()


def Bds_cal(x):
    ep = [0.5, 1.0, 1.5, 2.0]
    rangg = list(range(2,9))
    collstat = {}
    collpvalue = {}

    for n in ep:
        s, p = bds(df.VIX,  max_dim=8, epsilon=n)
        collstat[n] = s.round(3)
        collpvalue[n] = p
        
    stat_table = pd.DataFrame(collstat, index=rangg)
    pvalue_table = pd.DataFrame(collpvalue, index=rangg)
    
    return stat_table, pvalue_table

stats, pvalue = Bds_cal(df.VIX)
print(stats, pvalue, sep="\n\n")
