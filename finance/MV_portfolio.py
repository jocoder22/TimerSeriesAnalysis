
# https://www.machinelearningplus.com/machine-learning/portfolio-optimization-python-example/

#!/usr/bin/env python
# Load Packages
import numpy as np
import pandas as pd
from datetime import datetime
import pandas_datareader as pdr
import matplotlib.pyplot as plt
%matplotlib inline

porfolio = ['AAPL', 'ABT', 'AIG','AMAT']
startdate = datetime(2018,1,1)

def portfolioAnalysis(porf):
  
    allstocks = pdr.get_data_yahoo(porf, startdate)['Adj Close']
    cov_matrix = np.log(allstocks/allstocks.shift()).cov()


    # Yearly returns for individual companies
    yearly_er = allstocks.resample('Y').last().pct_change().mean()


    p_ret = [] # Define an empty array for portfolio returns
    p_vol = [] # Define an empty array for portfolio volatility
    p_weights = [] # Define an empty array for asset weights

    num_assets = len(allstocks.columns)
    num_portfolios = 20000
    np.random.seed(0)

    for portfolio in range(num_portfolios):
        weights = np.random.random(num_assets)
        weights = weights/np.sum(weights)
        p_weights.append(weights)

        returns = np.dot(weights, yearly_er) # Returns are the product of individual expected returns of asset and its weights 
        p_ret.append(returns)

        var = cov_matrix.mul(weights, axis=0).mul(weights, axis=1).sum().sum()# Portfolio Variance
        sd = np.sqrt(var) # Daily standard deviation
        ann_sd = sd*np.sqrt(250) # Annual standard deviation = volatility
        p_vol.append(ann_sd)

    data = {'Returns':p_ret, 'Volatility':p_vol}

    for counter, symbol in enumerate(allstocks.columns.tolist()):
      data[symbol+' weight'] = [w[counter] for w in p_weights]

    portfolios  = pd.DataFrame(data)

    # mininum variance portfolio
    min_vol_port = portfolios.iloc[portfolios['Volatility'].idxmin()]

    # max return portfolio
    max_ret_port = portfolios.iloc[portfolios['Returns'].idxmax()]


    # Finding the optimal portfolio
    rf = 0.01 # risk factor
    optimal_risky_port = portfolios.iloc[((portfolios['Returns']-rf)/portfolios['Volatility']).idxmax()]


    # Plot efficient frontier
    # portfolios.plot.scatter(x='Volatility', y='Returns', marker='o', s=10, alpha=0.3, grid=True, figsize=[10,10])

    # Plotting optimal portfolio
    # plt.figure(figsize=(14,10))
    plt.subplots(figsize=(14, 10))
    plt.scatter(portfolios['Volatility'], portfolios['Returns'],marker='o', s=10, alpha=0.3)
    plt.scatter(min_vol_port[1], min_vol_port[0], color='r', marker='*', s=500)
    plt.scatter(max_ret_port[1], max_ret_port[0], color='y', marker='*', s=500)
    plt.scatter(optimal_risky_port[1], optimal_risky_port[0], color='g', marker='*', s=500)
    plt.show()
    print("\n\n\n")
    
    print(f"Minimal Volatility Portfolio")
    print(min_vol_port, end="\n\n")
    print(f"Maximal Return Portfolio")
    print(max_ret_port, end="\n\n")
    print(f"Optimal Risky Portfolio")
    print(optimal_risky_port, end="\n\n")

    return min_vol_port, max_ret_port, optimal_risky_port
  
ddd = df.tail(1); bbb = df.head(1)
fff = pd.concat([bbb, ddd])
mmm = fff.pct_change().mean()


# ['CHPT', 'QS', 'NIO', 'XPEV', 'LI', 'NKLA', 'BLNK']
# ['SPSC']
