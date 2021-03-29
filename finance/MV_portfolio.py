#!/usr/bin/env python
# Load Packages
import numpy as np
import pandas as pd
from datetime import datetime
from pandas_datareader import data
import matplotlib.pyplot as plt
%matplotlib inline

porfolio = ['AAPL', 'ABT', 'AIG','AMAT']
startdate = datetime(2018,1,1)

def portfolioAnalysis(porf):
  
  allstocks = pdr.get_data_yahoo(porf, startdate)['Adj Close']
  cov_matrix = np.log(allstocks/allstocks.shift()).cov()
  corr_matrix = np.log(allstocks/allstocks.shift()).corr()
  
  
  p_ret = [] # Define an empty array for portfolio returns
  p_vol = [] # Define an empty array for portfolio volatility
  p_weights = [] # Define an empty array for asset weights

  num_assets = len(allstocks.columns)
  num_portfolios = 20000
    
  for portfolio in range(num_portfolios):
      weights = np.random.random(num_assets)
      weights = weights/np.sum(weights)
      p_weights.append(weights)

      returns = np.dot(weights, ind_er) # Returns are the product of individual expected returns of asset and its weights 
      p_ret.append(returns)
      var = cov_matrix.mul(weights, axis=0).mul(weights, axis=1).sum().sum()# Portfolio Variance
      sd = np.sqrt(var) # Daily standard deviation
      ann_sd = sd*np.sqrt(250) # Annual standard deviation = volatility
      p_vol.append(ann_sd)

    data = {'Returns':p_ret, 'Volatility':p_vol}



  

