import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader as pdr

from datetime import datetime
# startdate = datetime(2010,11,1)
# enddate = datetime(2019,1,30)
startdate = datetime(2019, 1, 1)
# enddate = datetime(2020, 12, 31)

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


