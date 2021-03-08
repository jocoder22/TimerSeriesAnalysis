#!/usr/bin/env python
import os
import numpy as np
import pandas as pd
from pathlib import Path

def tickimbalaneT(stock,price):
  stock['PriceChange'] = stock[price].diff()
  stock['PriceChange_1'] = stock.PriceChange.shift(periods = -1)
  stock['b_t'] = stock[["PriceChange_1", "PriceChange"]].apply(lambda x: x[1] if x[0] == 0 else np.absolute(x[1])/x[1] , axis=1)
