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

from printdescribe import changepath

from mmodules.load_Data import _loadClean

datapath = r"E:\TimerSeriesAnalysis\Credit_Risk_Modelling\Data"

sns.set_style("darkgrid", {"grid.color": ".6", "grid.linestyle": ":"})
sp = {"end":"\n\n\n", "sep":"\n\n"}

credit = _loadClean()
print(credit.head())

# # Create the X and y data sets
X1_train = credit["person_income  person_emp_length  loan_amnt".split()]
X2_train = credit["person_income  loan_percent_income  cb_person_cred_hist_length".split()]
y_train = credit[["loan_status"]]

# Print the first five rows of each training set
print(X1_train.head())
print(X2_train.head())

# Create and train a model on the first training data
clf_logistic1 = LogisticRegression(solver='lbfgs').fit(X1_train, np.ravel(y_train))

# Create and train a model on the second training data
clf_logistic2 = LogisticRegression(solver='lbfgs').fit(X2_train, np.ravel(y_train))

# Print the coefficients of each model
print(clf_logistic1.coef_, **sp)
print(clf_logistic2.coef_, **sp)


# Create the X and y data sets
y = credit[["loan_status"]]
Xraw = credit.drop(columns =["loan_status"])
scaler = MinMaxScaler()

#################### One-hot encoding credit data ###################
# Create two data sets for numeric and non-numeric data
cred_num = Xraw.select_dtypes(exclude=['object'])
cred_str = Xraw.select_dtypes(include=['object'])

# One-hot encode the non-numeric columns
cred_str_onehot = pd.get_dummies(cred_str, drop_first=True)
cred_str_onehot2 = pd.get_dummies(cred_str)

Xs = scaler.fit_transform(cred_num)
XX = pd.DataFrame(Xs, columns=cred_num.columns)

# Union the one-hot encoded columns to the numeric ones
Xall = pd.concat([XX, cred_str_onehot], axis=1)
Xall2 = pd.concat([XX, cred_str_onehot2], axis=1)

# Combine all data and save for analysis
###########################################
# alldata = pd.concat([y, Xall], axis=1)
# alldata2 = pd.concat([y, Xall2], axis=1)
# with changepath(datapath):
#     alldata.to_csv("AnalysisData.csv", index=False)
#     alldata2.to_csv("AnalysisData2.csv", index=False)
########################################################


# Use test_train_split to create the training and test sets
X_train, X_test, y_train, y_test = train_test_split(XX, y, test_size=.25, random_state=149, stratify=y)

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