#!/usr/bin/env python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import xgboost as xgb

from sklearn.model_selection import train_test_split

from mmodules.load_Data import _loadAnalysis2, _loadClean
from sklearn.model_selection import cross_val_score

sns.set_style("darkgrid", {"grid.color": ".6", "grid.linestyle": ":"})
sp = {"end":"\n\n\n", "sep":"\n\n"}

credit = _loadAnalysis2()

# Create the X and y data sets
y = credit["loan_status"]
X = credit.drop(columns=["loan_status"])

# Use test_train_split to create the training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.25, random_state=149, stratify=y)

# instantiate the model and fit
params = {'objective': 'binary:logistic', 'seed': 123, 'eval_metric': 'auc'}

# Set the values for number of folds and stopping iterations
n_folds = 5
early_stopping = 20

# Create the DTrain matrix for XGBoost
DTrain = xgb.DMatrix(X_train, label = y_train)

# Create the data frame of cross validations
cv_df = xgb.cv(params, DTrain, num_boost_round = 5, nfold=n_folds,
            early_stopping_rounds=early_stopping)

# Print the cross validations data frame
print(cv_df, **sp)


# Create large numbers for both nfold and num_boost_round
# look at this data to see what the AUC are, 
# and check to see if they reach 1.0, 
# Nope, large numbers dont necessarily improve accuracy
cv_results_big = xgb.cv(params, DTrain, num_boost_round = 600, nfold=10,
            shuffle = True)

# Print the first five rows of the CV results data frame
print(cv_results_big.head(), **sp)

# Calculate the mean of the test AUC scores
print(np.mean(cv_results_big["test-auc-mean"]).round(2), **sp)

# Plot the test AUC scores for each iteration
plt.plot(cv_results_big["test-auc-mean"])
plt.title('Test AUC Score Over 600 Iterations')
plt.xlabel('Iteration Number')
plt.ylabel('Test AUC Score')
plt.show()

# Create a gradient boosted tree model using two hyperparameters
gbt = xgb.XGBClassifier(learning_rate = 0.1, max_depth = 7)

# Calculate the cross validation scores for 4 folds
cv_scores = cross_val_score(gbt, X_train, np.ravel(y_train), cv = 4)

# Print the cross validation scores
print(cv_scores, **sp)

# Print the average accuracy and standard deviation of the scores
print("Average accuracy: %0.2f (+/- %0.2f)" % (cv_scores.mean(),
                                              cv_scores.std() * 2), **sp)