#!/usr/bin/env python
import numpy as np
import pandas as pd

from printdescribe import changepath

datapath = r"E:\TimerSeriesAnalysis\Intro_Portfolio_Risk_Mgt\Data"

sp = {"end":"\n\n", "sep":"\n\n"}

with changepath(datapath):
    data = pd.read_csv("portfolio.csv", index_col="Date")
    print(data.head())



