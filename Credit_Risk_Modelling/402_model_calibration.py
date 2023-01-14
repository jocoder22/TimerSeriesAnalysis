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
from sklearn.calibration import calibration_curve

from mmodules.load_Data import _loadAnalysis, _loadClean

sns.set_style("darkgrid", {"grid.color": ".6", "grid.linestyle": ":"})
sp = {"end":"\n\n\n", "sep":"\n\n"}

credit = _loadAnalysis()

# Create the X and y data sets
y = credit["loan_status"]
X = credit.drop(columns=["loan_status"])

# Use test_train_split to create the training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.30, random_state=149, stratify=y)

# create the models
gbt = xgb.XGBClassifier(learning_rate = 0.2, max_depth = 10)
clf_logistic = LogisticRegression(solver='lbfgs')

names = ["Xboost", "logmodel"]
preds_cali = pd.DataFrame()

for i, model in enumerate([gbt, clf_logistic]):
    # instantiate the model and fit
    clf = model.fit(X_train, np.ravel(y_train))

    # Predict with a model
    preds_ = clf.predict_proba(X_test)[:,1]

    frac, mean_ = calibration_curve(y_test, preds_, n_bins=20)
    preds_cali[f"{names[i]}_frac_of_pos"] = frac
    preds_cali[f"{names[i]}_Mean_pred"] = mean_


# Create the calibration curve plot with the guideline
plt.plot([0, 1], [0, 1], 'k:', label='Perfectly calibrated')
plt.plot(preds_cali["logmodel_Mean_pred"], preds_cali["logmodel_frac_of_pos"], 's-', label='Logistic Regression', color="g")
plt.plot(preds_cali["Xboost_Mean_pred"], preds_cali["Xboost_frac_of_pos"], 's-', label='XGBoost Model', color="r")      
plt.ylabel('Fraction of positives')
plt.xlabel('Average Predicted Probability')
plt.legend()
plt.title('Calibration Curve')
plt.show()
