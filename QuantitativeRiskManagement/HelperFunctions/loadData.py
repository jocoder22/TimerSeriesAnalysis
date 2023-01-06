#!/usr/bin/env python
import numpy as np
import pandas as pd

from printdescribe import changepath

datapath = r"E:\TimerSeriesAnalysis\QuantitativeRiskManagement\Data"


def _loadAssets():
    with changepath(datapath):
        portfolio_ = pd.read_csv("assetsData.csv", parse_dates=True, index_col="Date")

    return portfolio_




