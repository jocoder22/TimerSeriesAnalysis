#!/usr/bin/env python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import xgboost as xgb

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# from sklearn.metrics import classification_report, precision_recall_fscore_support
# from sklearn.metrics import roc_auc_score, roc_curve
# from sklearn.calibration import calibration_curve

from mmodules.load_Data import _loadAnalysis, _loadClean

sns.set_style("darkgrid", {"grid.color": ".6", "grid.linestyle": ":"})
sp = {"end":"\n\n\n", "sep":"\n\n"}


# Acceptance rate: This is a percentage of new loans that we accept with the goal 
# of keeping the number of defaults in a portfolio below a certain number.

# If we want to accept 85% of all loans with the lowest probabilities of default, then 
# our acceptance rate is 85%. This means we reject 15% of all loans with the highest 
# probabilities of default. Instead of setting a threshold value, we want to calculate 
# it to separate the loans we accept using our acceptance rate from the loans we reject.

# Even though we've calculated an acceptance rate for our loans and set a threshold, there 
# will still be some defaults in our accepted loans, thus bad loans.
# The bad rate is the percentage of accepted loans which are actually defaults. 
# The calculation for the bad rate is the number of defaults in our accepted loans
# divided by the total number of accepted loans

# load analysis data
credit = _loadAnalysis()

# load clean data
credit2 = _loadClean()

# Create the X and y data sets
y = credit["loan_status"]
X = credit.drop(columns=["loan_status"])

# Use test_train_split to create the training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.30, random_state=149, stratify=y)

# create the models
gbt = xgb.XGBClassifier(learning_rate = 0.2, max_depth = 10)
clf_logistic = LogisticRegression(solver='lbfgs')

names = ["Xboost", "logmodel"]
params = [{"color":"blue"}, {"color":"red", "alpha":0.4}]
preds_proba_ = pd.DataFrame(y_test.values, columns=["Actual"], index=y_test.index)
preds_proba = preds_proba_.merge(credit2['loan_amnt'],
                left_index=True, right_index=True )
datamap = {1:"Defaults", 0:"Non Defaults"}

# Print the statistics of the loan amount column
print(preds_proba["loan_amnt"].describe(), **sp)

# Store the average loan amount
avg_loan = np.mean(preds_proba["loan_amnt"])

fig, ax = plt.subplots()
for i, model in enumerate([gbt, clf_logistic]):
    # instantiate the model and fit
    clf = model.fit(X_train, np.ravel(y_train))

    # Predict with a model
    preds_proba[names[i]] = clf.predict_proba(X_test)[:,1]

    # Calculate the threshold for a 85% acceptance rate
    threshold_85 = np.quantile(preds_proba[names[i]], 0.85)

    # Apply acceptance rate threshold
    preds_proba[f"{names[i]}_rate"] = preds_proba[names[i]].apply(lambda x: 1 if x > threshold_85 else 0)

    # Create a subset of only accepted loans
    accepted_loans = preds_proba[preds_proba[f"{names[i]}_rate"] == 0]

    # Calculate the bad rate
    print(f"This is for {names[i]}")
    print(f"Bad rate: {np.mean(accepted_loans['Actual'] == 1) * 100:.2f}%", **sp)

    # Print the counts of loan status after the threshold
    print(preds_proba[f"{names[i]}_rate"].map(datamap).value_counts(), **sp)

    # Plot the predicted probabilities of default
    plt.hist(preds_proba[names[i]], bins = 40, **params[i], label=names[i])

    # Add a reference line to the plot for the threshold
    plt.axvline(x = threshold_85, color = params[i]["color"])

plt.legend()
plt.show()

# Check the statistics of the probabilities of default
print(preds_proba.describe(), **sp)
print(preds_proba.info(), preds_proba.head(), **sp)
print(f"Bad rate without Model: {np.mean(preds_proba['Actual'] == 1) * 100:.2f}%", **sp)

for i, name in enumerate(["Xboost_rate","logmodel_rate"]):
    # Set the formatting for currency, and print the cross tab
    pd.options.display.float_format = '${:,.2f}'.format

    losstable = pd.crosstab(preds_proba['Actual'].map(datamap),
                    preds_proba[name].map(datamap),
                 ).apply(lambda x: x * avg_loan, axis = 0)

    losstable2 = pd.crosstab(preds_proba['Actual'].map(datamap),
                    preds_proba[name].map(datamap), values = preds_proba["loan_amnt"] * 1.0,
                          aggfunc=sum)

    print(f"This is for {names[i]}")
    for b in [losstable, losstable2]:
        print(b,"\n", f"Total loss: ${b.iloc[1,0] + b.iloc[0, 1]:,.2f}",\
                    f"Actual loss: ${b.iloc[1,0]:,.2f}", \
                    f"Missed Opportunity: ${b.iloc[0, 1]:,.2f}", sep="\n", end="\n\n")

pd.reset_option('^display.', silent=True)

print(preds_proba.head())