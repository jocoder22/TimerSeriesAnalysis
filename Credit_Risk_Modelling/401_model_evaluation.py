#!/usr/bin/env python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import xgboost as xgb

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

from sklearn.metrics import classification_report, precision_recall_fscore_support
from sklearn.metrics import roc_auc_score, roc_curve

from mmodules.load_Data import _loadAnalysis, _loadClean

sns.set_style("darkgrid", {"grid.color": ".6", "grid.linestyle": ":"})
sp = {"end":"\n\n\n", "sep":"\n\n"}

credit = _loadAnalysis()

# Create the X and y data sets
y = credit["loan_status"]
X = credit.drop(columns=["loan_status"])

# Use test_train_split to create the training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.25, random_state=149, stratify=y)

# create the models
gbt = xgb.XGBClassifier(learning_rate = 0.2, max_depth = 10)
clf_logistic = LogisticRegression(solver='lbfgs')

names = ["Xboost", "logmodel"]
preds_df = pd.DataFrame()
preds_proba = pd.DataFrame()

for i, model in enumerate([gbt, clf_logistic]):
    # instantiate the model and fit
    model.fit(X_train, np.ravel(y_train))

    # Predict with a model
    preds_ = model.predict_proba(X_test)[:,1]
    preds_proba[names[i]] = preds_

    # Reassign loan status based on the threshold
    preds_df[names[i]] = [1 if x > 0.40 else 0 for x in preds_]

# Print the classification report and F-1 scores of the models
target_names = ['Non-Default', 'Default']

for i, name in enumerate(["Gradient Boost Model", "Logistic Model"]):
    print(f"This is for {name}:")
    # Print the classification report
    print(classification_report(y_test, preds_df[names[i]], target_names=target_names))
    
    # Print the default F-1 scores 
    print(precision_recall_fscore_support(y_test, preds_df[names[i]], average = 'macro')[2], **sp)

# ROC chart components
fallout_lr, sensitivity_lr, thresholds_lr = roc_curve(y_test, preds_proba["logmodel"])
fallout_gbt, sensitivity_gbt, thresholds_gbt = roc_curve(y_test, preds_proba["Xboost"])

# ROC Chart with both
plt.plot(fallout_lr, sensitivity_lr, color = 'blue', label='%s' % 'Logistic Regression')
plt.plot(fallout_gbt, sensitivity_gbt, color = 'green', label='%s' % 'GBT')
plt.plot([0, 1], [0, 1], linestyle='--', label='%s' % 'Random Prediction')
plt.title("ROC Chart for LR and GBT on the Probability of Default")
plt.xlabel('Fall-out')
plt.ylabel('Sensitivity')
plt.legend()
plt.show()

# Print the logistic regression AUC with formatting
print("Logistic Regression AUC Score: %0.2f" % roc_auc_score(y_test, preds_proba["logmodel"]))

# Print the gradient boosted tree AUC with formatting
print("Gradient Boosted Tree AUC Score: %0.2f" % roc_auc_score(y_test, preds_proba["Xboost"]))