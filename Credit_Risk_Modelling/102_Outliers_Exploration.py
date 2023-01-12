#!/usr/bin/env python
import numpy as np
import pandas as pd
import matplotlib.colors as mcc
import matplotlib.pyplot as plt
import seaborn as sns

from mmodules.load_Data import _load

sns.set_style("darkgrid", {"grid.color": ".6", "grid.linestyle": ":"})
sp = {"end":"\n\n\n", "sep":"\n"}

credit = _load()


# Generally with credit data, key columns like person_emp_length are of 
# high quality, but there is always room for error.
# Create the cross table for loan status, home ownership, and the max employment length
print(pd.crosstab(credit['loan_status'],credit['person_home_ownership'],
                  values=credit['person_emp_length'], aggfunc='max'))

# Create an array of indices where employment length is greater than 60
indices = credit[credit['person_emp_length'] > 60].index

# Drop the records from the data based on the indices and create a new dataframe
credit_new = credit.drop(indices)

# Create the cross table from earlier and include minimum employment length
print(pd.crosstab(credit_new['loan_status'],credit_new['person_home_ownership'],
            values=credit_new['person_emp_length'], aggfunc=['min','max']))

# Create the scatter plot for age and amount
plt.title("Scatter plot: Age and Loan Amount")
plt.scatter(credit["person_age"], credit["loan_amnt"], c='blue', alpha=0.5)
plt.xlabel("Person Age")
plt.ylabel("Loan Amount")
plt.show()


# Use Pandas to drop the record from the data frame and create a new one
credit_new = credit.drop(credit[credit["person_age"] > 100].index)

# Create a scatter plot of age and interest rate
color = ["blue","red"]
colors = {0:'blue', 1:'red'}
fig, ax = plt.subplots()
scatter = ax.scatter(credit_new["person_age"], credit_new["loan_int_rate"],
            # c = credit_new['loan_status'].map(colors),
            c = credit_new['loan_status'],
            cmap = mcc.ListedColormap(color),
            # cmap = "seismic", s = 120,
            alpha=0.5)
           
plt.xlabel("Person Age")
plt.ylabel("Loan Interest Rate")
handles, labels = scatter.legend_elements()
plt.legend(handles=handles, labels=("Non Defaults", "Defaults"), 
            fontsize=20, loc="upper right", #title="Loan Status", 
            title="$\\bf{Loan Status}$", title_fontsize=22,
            prop={'size': 18, 'style': 'italic'})
plt.title("Person Age Vs Loan Interest Rate")
plt.show()