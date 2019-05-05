#!/usr/bin/env python
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('ggplot')

import datetime
from datetime import date
from datetime import datetime
from datetime import timedelta


from iexfinance.stocks import get_historical_intraday, get_historical_data
