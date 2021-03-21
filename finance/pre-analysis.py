import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.decomposition import PCA
import bisect 

from datetime import datetime
from printdescribe import changepath

with changepath(path1):
    data = pd.read_csv("spy_vix.csv")