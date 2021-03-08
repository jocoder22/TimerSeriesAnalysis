#!/usr/bin/env python
import os
import numpy as np
import pandas as pd
from printdescribe print2

df = pd.DataFrame({
    'a': [4, 5, 6, 7, 9, 9,-30, -50, 0, 0 , 15, 10],
    'b': [10, 20, 30, 40,0, 0, -30, -50, 0, 0 , 15, 10],
    'c': [100, 50, 50, 10, 40, 40, -30, -50, 0, 0 , 15, 10]})

def tickimbalaneT(stock, price):
  stock['PriceChange'] = stock[price].diff()
  stock['PriceChange_Abs'] = stock['PriceChange'].abs()/stock['PriceChange']
  stock['bt_1'] = stock.PriceChange_Abs.shift(periods = 1)
  stock['b_t'] = stock[["bt_1", "PriceChange_Abs", "PriceChange"]].apply(lambda x: x[0] if x[2] == 0 else x[1] , axis=1)
  stock.drop(columns = ["bt_1", "PriceChange_Abs", "PriceChange"], inplace=True)
  

tickimbalaneT(df,'c')
print2(df)
