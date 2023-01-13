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

from mmodules.load_Data import _loadAnalysis, _loadClean

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

# Create predictions of probability for loan status using test data
preds = clf_logistic.predict_proba(X_test)

# Create a dataframe for the probabilities of default
preds_df = pd.DataFrame(preds[:,1], columns = ['prob_default'])

# Reassign loan status based on the threshold
preds_df["loan_status"] = preds_df["prob_default"].apply(lambda x: 1 if x > 0.50 else 0)

# Print the confusion matrix
print(confusion_matrix(y_test,preds_df["loan_status"]), **sp)

# Set the threshold for defaults to 0.5
preds_df["loan_status"] = preds_df["prob_default"].apply(lambda x: 1 if x > 0.40 else 0)

# Print the confusion matrix
print(confusion_matrix(y_test,preds_df["loan_status"]), **sp)

# load clean data
credit2 = _loadClean()
avg_loan_amnt = credit2['loan_amnt'].mean()

# Store the number of loan defaults from the prediction data
num_defaults = preds_df["loan_status"].value_counts()[1]

# Store the default recall from the classification report
default_recall = precision_recall_fscore_support(y_test,preds_df["loan_status"])[1][1]

# Calculate the estimated impact of the new default recall rate
print(avg_loan_amnt * num_defaults * (1 - default_recall), **sp)

# Threshold selection
thresh = np.linspace(0.0, 1.0, 21)
def_recalls = []
nondef_recalls = []
accs = []

for threshold in thresh:
        preds_df["loan_status"] = preds_df["prob_default"].apply(lambda x: 1 if x > threshold else 0)
        accs.append(accuracy_score(y_test,preds_df["loan_status"]))
        def_recalls.append(precision_recall_fscore_support(y_test,preds_df["loan_status"])[1][1])
        nondef_recalls.append(precision_recall_fscore_support(y_test,preds_df["loan_status"])[1][0])

# plot line chart
plt.title("Threshold selection")
plt.plot(thresh,def_recalls)
plt.plot(thresh,nondef_recalls)
plt.plot(thresh,accs)
plt.xlabel("Probability Threshold")
plt.legend(["Default Recall","Non-default Recall","Model Accuracy"])
plt.show()