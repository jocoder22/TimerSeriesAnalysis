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
