#!/usr/bin/env python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import xgboost as xgb

from sklearn.model_selection import train_test_split

from mmodules.load_Data import _loadAnalysis2, _loadClean

sns.set_style("darkgrid", {"grid.color": ".6", "grid.linestyle": ":"})
sp = {"end":"\n\n\n", "sep":"\n\n"}

credit = _loadAnalysis2()

# Create the X and y data sets
y = credit["loan_status"]
X = credit.drop(columns=["loan_status"])

# Use test_train_split to create the training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.25, random_state=149, stratify=y)
X_train2 = X_train[['person_income','loan_int_rate', 'loan_percent_income','loan_amnt',
                  'person_home_ownership_MORTGAGE','loan_grade_F']]

# instantiate the model and fit
clf_gbt = xgb.XGBClassifier().fit(X_train, np.ravel(y_train))
clf_gbt2 = xgb.XGBClassifier().fit(X_train2, np.ravel(y_train))

# Print the column importances from the model
print(clf_gbt.get_booster().get_score(importance_type = 'weight'), **sp)
print(clf_gbt2.get_booster().get_score(importance_type = 'weight'), **sp)

# Plot the column importance for this model
xgb.plot_importance(clf_gbt, importance_type = 'weight')
plt.show()

# Plot the column importance for this model
xgb.plot_importance(clf_gbt2, importance_type = 'weight')
plt.show()

# create x train with some features
X_train4 = X_train[['loan_int_rate','person_emp_length']]
X_train3 = X_train[['person_emp_length','loan_int_rate','loan_percent_income']]

# Train a model on the X data with 3 columns
clf_gbt3 = xgb.XGBClassifier().fit(X_train3,np.ravel(y_train))

# Plot the column importance for this model
xgb.plot_importance(clf_gbt3, importance_type = 'weight')
plt.show()

# Train a model on the X data with 2 columns
clf_gbt4 = xgb.XGBClassifier().fit(X_train4,np.ravel(y_train))

# Plot the column importance for this model
xgb.plot_importance(clf_gbt4, importance_type = 'weight')
plt.show()

# create x train with some features
X_test4 = X_test[['loan_int_rate','person_emp_length']]
X_test3 = X_test[['person_emp_length','loan_int_rate','loan_percent_income']]

# Predict the loan_status using each model
gbt_preds = clf_gbt3.predict(X_test3)
gbt2_preds = clf_gbt4.predict(X_test4)

# Print the classification report of the first model
target_names = ['Non-Default', 'Default']
print("Model with 'person_emp_length','loan_int_rate','loan_percent_income'")
print(classification_report(y_test, gbt_preds, target_names=target_names), **sp)

# Print the classification report of the second model
print("Model with 'loan_int_rate','person_emp_length'")
print(classification_report(y_test, gbt2_preds, target_names=target_names), **sp)