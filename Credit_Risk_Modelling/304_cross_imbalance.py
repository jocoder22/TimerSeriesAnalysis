#!/usr/bin/env python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import xgboost as xgb

from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.metrics import roc_auc_score, classification_report

from mmodules.load_Data import _loadAnalysis2, _loadClean


sns.set_style("darkgrid", {"grid.color": ".6", "grid.linestyle": ":"})
sp = {"end":"\n\n\n", "sep":"\n\n"}

credit = _loadAnalysis2()

# Create the X and y data sets
y = credit["loan_status"]
X = credit.drop(columns=["loan_status"])

# Use test_train_split to create the training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.25, random_state=149, stratify=y)

# combine the train X and y
X_y_train = pd.concat([X_train.reset_index(drop = True),
                       y_train.reset_index(drop = True)], axis = 1)

count_nondefault, count_default = X_y_train['loan_status'].value_counts()

print("Training data imbalace:")
print(f"Count of Non defaults: {count_nondefault}\n  Count of defaults {count_default}", **sp)

# Create data sets for defaults and non-defaults
nondefaults = X_y_train[X_y_train["loan_status"] == 0]
defaults = X_y_train[X_y_train["loan_status"] == 1]

# Undersample the non-defaults
nondefaults_under = nondefaults.sample(count_default)

# Concatenate the undersampled nondefaults with defaults
X_y_train_under = pd.concat([nondefaults_under.reset_index(drop = True),
                             defaults.reset_index(drop = True)], axis = 0)

# Print the value counts for loan status
print("Balanced Training Data")
print(X_y_train_under['loan_status'].value_counts(), **sp)

balance_X = X_y_train_under.drop(columns =['loan_status'])
balance_y = X_y_train_under['loan_status']

data_list = [[X_train, y_train],[balance_X, balance_y]]
labels = ['Unbalanced Data', 'Balanced Data']
meanAcc, stdAcc, aucScore = [], [], []

for i, x in enumerate(data_list):
    # Create a gradient boosted tree model using two hyperparameters
    gbt = xgb.XGBClassifier(learning_rate = 0.2, max_depth = 10)

    # Calculate the cross validation scores for 4 folds
    cv_scores = cross_val_score(gbt, x[0], np.ravel(x[1]), cv = 5)

    gbt_preds = gbt.fit(x[0], np.ravel(x[1])).predict(X_test)
    aucScore.append(roc_auc_score(y_test, gbt_preds))

    # Check the classification reports
    target_names = ['Non-Default', 'Default']
    print(f"Classification report for {labels[i]}")
    print(classification_report(y_test, gbt_preds, target_names=target_names), **sp)

    meanAcc.append(cv_scores.mean()); stdAcc.append(cv_scores.std())


for i, v in enumerate(labels):
    # Print the average accuracy and standard deviation of the scores
    print(f"Average accuracy for {v}: {meanAcc[i]:.2f} (+/- {stdAcc[i] * 2:.2f}),\
      AUC = {aucScore[i]:.2f}")

print(**sp)

