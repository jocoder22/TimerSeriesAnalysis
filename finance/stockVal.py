#!/usr/bin/env python
import requests
import pandas as pd
import pandas_datareader as pdr
import fix_yahoo_finance as yf
import statsmodels.tsa.stattools as ts
import time
import string

from printdescribe import changepath
from datetime import datetime, date
from bs4 import BeautifulSoup

asset = yf.download("GOOG", start="2000 01 01", end="2021 01 31")
ts.adfuller(asset['Adj Close'])



