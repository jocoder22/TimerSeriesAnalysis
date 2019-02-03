import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import datetime
import pandas_datareader as pdr


from statsmodels.tsa.stattools import acf
from statsmodels.graphics.tsaplots import plot_acf


""" 
B         business day frequency
C         custom business day frequency (experimental)
D         calendar day frequency
W         weekly frequency
M         month end frequency
SM        semi-month end frequency (15th and end of month)
BM        business month end frequency
CBM       custom business month end frequency
MS        month start frequency
SMS       semi-month start frequency (1st and 15th)
BMS       business month start frequency
CBMS      custom business month start frequency
Q         quarter end frequency
BQ        business quarter endfrequency
QS        quarter start frequency
BQS       business quarter start frequency
A         year end frequency
BA, BY    business year end frequency
AS, YS    year start frequency
BAS, BYS  business year start frequency
BH        business hour frequency
H         hourly frequency
T, min    minutely frequency
S         secondly frequency
L, ms     milliseonds
U         microseconds
N, us     nanoseconds
"""
path = 'C:\\Users\\Jose\\Desktop\\TimerSeriesAnalysis'
os.chdir(path)

starttime = datetime.datetime(2006, 8, 1)
endtime = datetime.datetime(2017, 11, 1)

symbol = 'HRB'
HRB = pdr.get_data_yahoo(symbol, starttime, endtime)

HRB = HRB.resample(rule='QS').first()
returns = HRB.pct_change()
differ = HRB.diff()

# print(HRB.head())
print(returns.head())


differ = differ.dropna()
print(differ.head())
differ['Adj Close'].plot()
plt.show()

HRB = pd.read_csv('HRB.csv', parse_dates=True, index_col='Quarter')
HRB['Earnings'].plot()
plt.show()

print(HRB.head())
# Compute the acf array of HRB
acf_array = acf(HRB)
print(acf_array)

# Plot the acf function
plot_acf(HRB)
plt.show()




