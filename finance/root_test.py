#!/usr/bin/env python
import os
import numpy as np
import pandas as pd

# Kwiatkowski-Phillips-Schmidt-Shin (KPSS) test (Kwiatkowski, Phillips, Schmidt, & Shin, 1992). 
# In this test, the null hypothesis is that the data are stationary, 
# and we look for evidence that the null hypothesis is false.

# Kwiatkowski, D., Phillips, P. C. B., Schmidt, P., & Shin, Y. (1992). 
# Testing the null hypothesis of stationarity against the alternative of a unit root: How sure are we that economic time series have a unit root? 
# Journal of Econometrics, 54(1-3), 159–178. https://doi.org/10.1016/0304-4076(92)90104-Y
