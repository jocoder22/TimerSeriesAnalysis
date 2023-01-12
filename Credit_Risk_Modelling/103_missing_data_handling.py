#!/usr/bin/env python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from mmodules.load_Data import _load

sns.set_style("darkgrid", {"grid.color": ".6", "grid.linestyle": ":"})
sp = {"end":"\n\n\n", "sep":"\n"}

credit = _load()

# Print a null value column array
print(credit.columns[credit.isnull().any()], credit.shape, **sp)

# Print the top five rows with nulls for employment length
print(credit[credit["person_emp_length"].isnull()].head(), **sp)

# Impute the null values with the median value for all employment lengths
credit['person_emp_length'].fillna((credit['person_emp_length'].median()), inplace=True)

# Create a histogram of employment length
n, bins, patches = plt.hist(credit["person_emp_length"], bins='auto', color='blue')
plt.xlabel("Person Employment Length")
plt.show()

# Print the number of nulls
print(credit["loan_int_rate"].isnull().sum(), **sp)

# Store the array on indices
indices = credit[credit["loan_int_rate"].isnull()].index

# Save the new data without missing data
credit_clean = credit.drop(indices)
print(credit_clean.shape, **sp)

