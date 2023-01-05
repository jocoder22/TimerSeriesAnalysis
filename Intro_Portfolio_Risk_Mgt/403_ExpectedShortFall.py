import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict

import mmodules.header as hd

# get our Fama French portfolio data
df = pd.read_pickle(os.path.join(hd.datapath, "Fama_French_PortfolioFull.pkl"))
# print(df.head(), df.tail(), df.columns, **hd.sp)

# Historical Value at Risk
# Value at Risk, often referred to as VaR, is a way to estimate the risk of
#  a single day negative price movement. VaR can be measured for any
#   given probability, or confidence level, but the most commonly quoted 
#   tend to be VaR(95) and VaR(99).

cols = ['S&P500', 'Portfolio_MSR', 'Portfolio_GMV', 'Portfolio_GMR']
VaRValues = defaultdict(list)

for col in cols:
    # Define the regression formula
    VaRValues['Model'].append(col)
    
    var_95 = np.percentile(df[col], 100 - 95)
    VaRValues['VaR'].append(f'{var_95:.3f}%')

    cvar_95 = df.loc[df[col] < var_95, col].mean()
    VaRValues['ExpectedShortFall(cVaR)'].append(f'{cvar_95:.3f}%')


    # Sort the returns for plotting
    sorted_rets = df[col].sort_values()

    # Plot the probability of each sorted return quantile
    plt.hist(sorted_rets, density=True, stacked=True)
    plt.title(f"Historical Distribution of {col} Returns")
    plt.ylabel("Probability")
    plt.xlabel("Returns (%)")

    # Denote the VaR 95 quantile
    plt.axvline(x=var_95, color='r', linestyle='-', label=f"VaR 95: {var_95:.2f}%")
    plt.axvline(x=cvar_95, color='b', linestyle='-', label=f'CVaR 95: {cvar_95:.2f}%')
    plt.legend()
    plt.show()

VaR_Results = pd.DataFrame(VaRValues)
print(VaR_Results, **hd.sp)




