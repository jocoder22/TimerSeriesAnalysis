#!/usr/bin/env python
import numpy as np
import pandas as pd

from printdescribe import changepath

datapath = r"E:\TimerSeriesAnalysis\QuantitativeRiskManagement\Data"


def _loadAssets(data, index = None):
    with changepath(datapath):
        portfolio_ = pd.read_csv(data, parse_dates=True, index_col=index)

    return portfolio_




