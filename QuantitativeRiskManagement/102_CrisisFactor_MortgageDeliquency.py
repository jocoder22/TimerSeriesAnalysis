#!/usr/bin/env python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from HelperFunctions.loadData import _loadAssets
from HelperFunctions.cleaners import _getCleanedData

# load the asset data
portfolio = _loadAssets("assetsData.csv", index="Date")
monthly_, quarterly_ = _getCleanedData()

ppf = pd.DataFrame(portfolio.iloc[0,:][4:])
ppf.columns = ["Rate"]
ppf.index.name = "Date"
print(ppf.index, ppf.head())


