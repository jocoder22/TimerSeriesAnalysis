#!/usr/bin/env python
import os
from pathlib import Path

def tickimbalaneT(stock):
  stock['tick'] = stock.price.diff()
  stock['b_t'] = stock.price.shift(periods, -1)
  stock['b_t'] = stock.b_t
  
