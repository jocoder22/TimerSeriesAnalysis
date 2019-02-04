import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import datasets
plt.style.use('ggplot')

from statsmodels.tsa.arima_process import ArmaProcess

# Plot 1: AR parameter = +0.9
plt.subplot(3,1,1)
ar1 = np.array([1, -0.9])
ma1 = np.array([1])
AR_object1 = ArmaProcess(ar1, ma1)
simulated_data_1 = AR_object1.generate_sample(nsample=1000)
plt.plot(simulated_data_1)
plt.title("AR parameter = +0.9")
plt.xticks([])

# Plot 2: AR parameter = 0.3
plt.subplot(3,1,2)
ar2 = np.array([1, -0.3])
ma2 = np.array([1])
AR_object2 = ArmaProcess(ar2, ma2)
simulated_data_2 = AR_object2.generate_sample(nsample=1000)
plt.plot(simulated_data_2)
plt.title("AR parameter = +0.3")
plt.xticks([])

# Plot 2: AR parameter = -0.9
plt.subplot(3,1,3)
ar3 = np.array([1, 0.9])
ma3 = np.array([1])
AR_object2 = ArmaProcess(ar3, ma3)
simulated_data_3 = AR_object2.generate_sample(nsample=1000)
plt.plot(simulated_data_2)
plt.title("AR parameter = -0.9")
plt.show()



fig, (ax1, ax2, ax3) = plt.subplots(nrows=3)
ax1.xaxis.tick_top()
ax2.axes.get_xaxis().set_visible(False)