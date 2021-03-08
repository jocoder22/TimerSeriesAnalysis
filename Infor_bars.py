#!/usr/bin/env python
import os
from pathlib import Path

def tickimbalaneT(stock):
  stock['PriceChange'] = stock.price.diff()
#   stock['PriceChange_Abs'] = stock['PriceChange'].abs()/stock['PriceChange']
  stock['PriceChange_1'] = stock.PriceChange.shift(periods, -1)
  
  stock['b_t'] = stock[["PriceChange_1", "PriceChange"]].apply(lambda x: x[1] if x[0] == 0 else x[1].abs()/x[1] , axis=1)
  
