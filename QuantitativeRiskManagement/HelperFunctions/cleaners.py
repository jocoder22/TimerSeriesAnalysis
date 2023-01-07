#!/usr/bin/env python
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from loadData import _loadAssets

datapath = r"E:\TimerSeriesAnalysis\QuantitativeRiskManagement\Data"

sp = {"end":"\n\n", "sep":"\n\n"}

def cagr(x):
    return (1 + x).prod() ** (1/len(x)) - 1


def _getCleanedData():
    """

    """
    dff = pd.DataFrame()
    dff2 = pd.DataFrame()
    for file_name in os.listdir(datapath):
        # print(file_name)
        if "cf" in file_name:
            # print(file_name)
            # load the asset data
            portfolio = _loadAssets(file_name, index=0)
            ppf = pd.DataFrame(portfolio.iloc[0,:][4:])
            ppf.columns = [f"Rate_{file_name}"]
            ppf.index.name = "Date"
            ppf.index = pd.to_datetime(ppf.index)
            # print(ppf.index, ppf.head(), **sp)

            dff = pd.concat([dff, ppf], axis=1, sort=False)

        if "fredQ" in file_name:
            # load the asset data
            ppf = _loadAssets(file_name, index=0)
            ppf.columns = [f"Rate_{file_name}"]
            ppf.index.name = "Date"
            ppf.index = pd.to_datetime(ppf.index)
            dff2 = pd.concat([dff2, ppf], axis=1, sort=False)

        if "year" in file_name:
            # load the asset data
            # ppf = _loadAssets(file_name, index=0).resample("m").mean()
            ppf = _loadAssets(file_name, index=0).resample("m").apply(cagr)
            ppf.columns = [f"Rate_{file_name}"]
            ppf.index.name = "Date"
            ppf.index = ppf.index.to_period('M')
            ppf.index = ppf.index.to_timestamp()
            # print(ppf.index, ppf.head(), **sp)
            dff = pd.concat([dff, ppf], axis=1, sort=False)

    return dff.dropna(), dff2


# pp, pp1 = _getCleanedData()

# print(pp.head(), pp1.head(), **sp)