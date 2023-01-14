#!/usr/bin/env python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.model_selection import train_test_split

from sklearn.metrics import roc_auc_score, accuracy_score, mean_squared_error as MSE
from sklearn.metrics import roc_curve
from sklearn.metrics import confusion_matrix, classification_report, precision_recall_fscore_support

from mmodules.load_Data import _loadAnalysis

sns.set_style("darkgrid", {"grid.color": ".6", "grid.linestyle": ":"})
sp = {"end":"\n\n\n", "sep":"\n\n"}

credit = _loadAnalysis()

# Create the X and y data sets
y = credit["loan_status"]
X = credit.drop(columns=["loan_status"])

# Use test_train_split to create the training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.25, random_state=149, stratify=y)

# Create and fit a logistic regression model
clf_logistic = LogisticRegression(solver='lbfgs')
clf_logistic.fit(X_train, np.ravel(y_train))

# Print the parameters of the model
print(clf_logistic.get_params(), **sp)

# Print the intercept of the model
print(clf_logistic.intercept_, **sp)

# Create predictions of probability for loan status using test data
preds = clf_logistic.predict_proba(X_test)

# Create dataframes of first five predictions, and first five true labels
preds_df = pd.DataFrame(preds[:,1][0:5], columns = ['prob_default'])
true_df = y_test.head()

# Concatenate and print the two data frames for comparison
print(pd.concat([true_df.reset_index(drop = True), preds_df], axis = 1), 
        clf_logistic.score(X_test, y_test),**sp)

# Create a dataframe for the probabilities of default
preds_df = pd.DataFrame(preds[:,1], columns = ['prob_default'])

# Reassign loan status based on the threshold
preds_df["loan_status"] = preds_df["prob_default"].apply(lambda x: 1 if x > 0.50 else 0)

# Print the row counts for each loan status
print(preds_df["loan_status"].value_counts(), **sp)

# Print the classification report
target_names = ['Non-Default', 'Default']
print(classification_report(y_test, preds_df['loan_status'], target_names=target_names), **sp)

# Print all the non-average values from the report
print(precision_recall_fscore_support(y_test, preds_df["loan_status"]), **sp)

# Print all the non-average values from the report
print(precision_recall_fscore_support(y_test, preds_df["loan_status"])[0], **sp)


# Plot the ROC curve of the probabilities of default
prob_default = preds[:, 1]
fallout, sensitivity, thresholds = roc_curve(y_test, prob_default)
plt.plot(fallout, sensitivity, color = 'darkorange')
# plt.plot(fallout, thresholds, color = 'g')
plt.plot([0, 1], [0, 1], linestyle='--')
plt.show()

# Compute the AUC and store it in a variable
auc = roc_auc_score(y_test, prob_default)
print(auc, **sp)