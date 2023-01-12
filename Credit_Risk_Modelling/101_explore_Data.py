#!/usr/bin/env python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from mmodules.load_Data import _load

sns.set_style("darkgrid", {"grid.color": ".6", "grid.linestyle": ":"})
sp = {"end":"\n\n\n", "sep":"\n"}

credit = _load()
print(credit.head(), credit.dtypes, credit.info(),  **sp)

# Look at the distribution of loan amounts with a histogram
plt.title("Distribution of Loan Amounts")
n, bins, patches = plt.hist(x=credit['loan_amnt'], bins='auto', color='blue',alpha=0.7, rwidth=0.85)
plt.xlabel("Loan Amount")
plt.show()

# Plot a scatter plot of income against age
plt.title("Scatter plot of income against age")
plt.scatter(credit['person_income'], credit['person_age'],c='blue', alpha=0.5)
plt.xlabel('Personal Income')
plt.ylabel('Persone Age')
plt.show()


# With cross tables, you get a high level view of selected columns 
# and even aggregation like a count or average. For most credit risk 
# models, especially for probability of default, columns like 
# person_emp_length and person_home_ownership are common to begin investigating.
# Create a cross table of the loan intent and loan status
print(pd.crosstab(credit["loan_intent"], credit["loan_status"], margins = True))

# Create a cross table of home ownership, loan status, and grade
print(pd.crosstab(credit["person_home_ownership"],[credit["loan_status"],credit["loan_grade"]]))

# Create a cross table of home ownership, loan status, and average percent income
print(pd.crosstab(credit["person_home_ownership"], credit["loan_status"],
              values=credit["loan_percent_income"], aggfunc="mean"))


# Create a box plot of percentage income by loan status
# Average percentage of income for defaults is higher. 
# Thus those recipients have a debt-to-income ratio that's already too high.
credit.boxplot(column = ["loan_percent_income"], by = "loan_status")
plt.title('Average Percent Income by Loan Status')
plt.suptitle('')
plt.show()             