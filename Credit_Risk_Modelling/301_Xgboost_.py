#!/usr/bin/env python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import xgboost as xgb

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

from sklearn.metrics import confusion_matrix, classification_report, precision_recall_fscore_support

from mmodules.load_Data import _loadAnalysis, _loadClean

sns.set_style("darkgrid", {"grid.color": ".6", "grid.linestyle": ":"})
sp = {"end":"\n\n\n", "sep":"\n\n"}

credit = _loadAnalysis()

# Create the X and y data sets
y = credit["loan_status"]
X = credit.drop(columns=["loan_status"])

# Use test_train_split to create the training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.25, random_state=149, stratify=y)

# instantiate the model and fit
clf_gbt = xgb.XGBClassifier().fit(X_train, np.ravel(y_train))

# Predict with a model
gbt_preds = clf_gbt.predict_proba(X_test)

# Create dataframes of first five predictions, and first five true labels
preds_df = pd.DataFrame(gbt_preds[:,1], columns = ['gbt_prob_default'])
true_pred = pd.concat([preds_df, y_test.reset_index()], axis = 1)

# print the two data frames for comparison
print(true_pred.head(), **sp)

# Create and fit a logistic regression model
clf_logistic = LogisticRegression(solver='lbfgs')
clf_logistic.fit(X_train, np.ravel(y_train))

# Predict the labels for loan status
lr_preds = clf_logistic.predict(X_test)

# Check the values created by the predict method
print(lr_preds, **sp)


# Create predictions of probability for loan status using test data
preds = clf_logistic.predict_proba(X_test)

# Create a dataframe for the probabilities of default
preds_df = pd.DataFrame(preds[:,1], columns = ['lr_prob_default'])

# combine prediction from both logistic and xgboost moedels
true_pred_all = pd.concat([preds_df, true_pred], axis = 1)
true_pred_all.set_index("index", inplace=True)

# load clean data
credit2 = _loadClean()

portfolio = true_pred_all.merge(credit2['loan_amnt'],
                left_index=True, right_index=True )

portfolio["lgd"] = 0.20

# Print the first five rows of the portfolio data frame
print(portfolio.head(), **sp)

# Create expected loss columns for each model using the formula
portfolio["gbt_expected_loss"] = portfolio["gbt_prob_default"] * portfolio["lgd"] * portfolio["loan_amnt"]
portfolio["lr_expected_loss"] = portfolio["lr_prob_default"] * portfolio["lgd"] * portfolio["loan_amnt"]

# Print the sum of the expected loss for lr
print(f'LR expected loss: {np.sum(portfolio["lr_expected_loss"])}', **sp)

# Print the sum of the expected loss for gbt
print(f'GBT expected loss: {np.sum(portfolio["gbt_expected_loss"])}', **sp)


# Predict the labels for loan status
gbt_preds = clf_gbt.predict(X_test)

# Check the values created by the predict method
print(gbt_preds, **sp)

# Print the classification report of the model
target_names = ['Non-Default', 'Default']
print("Gradient Boost Model")
print(classification_report(y_test, gbt_preds, target_names=target_names), **sp)
print("Logistic Model")
print(classification_report(y_test, lr_preds, target_names=target_names), **sp)