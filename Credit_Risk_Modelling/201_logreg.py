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
from sklearn.metrics import confusion_matrix, classification_report
 
 
sp = {'end':'\n\n', 'sep':'\n\n'}

from mmodules.load_Data import _loadClean

sns.set_style("darkgrid", {"grid.color": ".6", "grid.linestyle": ":"})
sp = {"end":"\n\n\n", "sep":"\n"}

credit = _loadClean()
print(credit.describe(), **sp)

# Create the X and y data sets
Xraw = credit[["loan_int_rate"]]
y = credit[["loan_status"]]

scaler = MinMaxScaler()
X = scaler.fit_transform(Xraw)

# Create and fit a logistic regression model
clf_logistic_single = LogisticRegression()
clf_logistic_single.fit(X, np.ravel(y))

# Print the parameters of the model
print(clf_logistic_single.get_params(), **sp)

# Print the intercept of the model
print(clf_logistic_single.intercept_, **sp)


###################### Multivariate logistic regression ######################
# Create X data for the model
X_multiraw = credit[["loan_int_rate" , "person_emp_length"]]

scaler = MinMaxScaler()
X_multi = scaler.fit_transform(X_multiraw)

# Create a set of y data for training
y = credit[["loan_status"]]

# Create and train a new logistic regression
clf_logistic_multi = LogisticRegression(solver='lbfgs').fit(X_multi, np.ravel(y))

# Print the intercept of the model
print(clf_logistic_multi.intercept_, **sp)



# Create the X and y data sets
Xraw = credit[['loan_int_rate','person_emp_length','person_income']]
y = credit[['loan_status']]

scaler = MinMaxScaler()
# scaler = StandardScaler()
X = scaler.fit_transform(Xraw)

# Use test_train_split to create the training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.25, random_state=149, stratify=y)

# Create and fit the logistic regression model
clf_logistic = LogisticRegression(solver='lbfgs').fit(X_train, np.ravel(y_train))

# Print the models coefficients
print(clf_logistic.coef_, clf_logistic.score(X_test, y_test), **sp)
