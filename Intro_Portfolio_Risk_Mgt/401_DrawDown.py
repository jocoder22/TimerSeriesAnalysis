import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict

import mmodules.header as hd

# get our Fama French portfolio data
df = pd.read_pickle(os.path.join(hd.datapath, "Fama_French_PortfolioFull.pkl"))
# print(df.head(), df.tail(), df.columns, **hd.sp)

# Plot the cumulative Returns and excess returns
title="Historical drawdown Plot"

# Historical drawdown
# The stock market tends to rise over time, but that doesn't mean that 
# you won't have periods of drawdown.

# Drawdown can be measured as the percentage loss from the highest cumulative historical point.

cols = ['S&P500', 'Portfolio_MSR', 'Portfolio_GMV', 'Portfolio_GMR']
dropDownValues = defaultdict(list)

for col in cols:
    # Define the regression formula
    dropDownValues['Model'].append(col)
    
    # Calculate the running maximum
    df['running_max'] = np.maximum.accumulate(df[col])

    # Ensure the value never drops below 1
    df.loc[df['running_max'] < 1, 'running_max'] = 1
    

    # Calculate the percentage drawdown
    df['drawdown'] = (df[col]/df.running_max) - 1

    maxdd = df['drawdown'].min()

    dropDownValues["Max_dropdown"].append(f'{maxdd:.3f}')


    # # Plot the results
    df['drawdown'].plot(title=title)
    plt.ylabel(ylabel = f"Historical drawdown for {col}")
    plt.show()

    df.drop(columns = ['running_max', 'drawdown'], inplace=True)
    # print(df, **hd.sp)

dropdownResults = pd.DataFrame(dropDownValues)
print(dropdownResults, **hd.sp)




