#!/usr/bin/env python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import xgboost as xgb


from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

from mmodules.load_Data import _loadAnalysis, _loadClean

sns.set_style("darkgrid", {"grid.color": ".6", "grid.linestyle": ":"})
sp = {"end":"\n\n\n", "sep":"\n\n"}

# load analysis data
credit = _loadAnalysis()

# load clean data
credit2 = _loadClean()

# Create the X and y data sets
y = credit["loan_status"]
X = credit.drop(columns=["loan_status"])

# Create dataframe with acceptance rates
strategyTable = pd.DataFrame(np.linspace(1.0, 0.05, 20), columns =["Accept_rate"])

# Use test_train_split to create the training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.30, random_state=149, stratify=y)

# create the models
gbt = xgb.XGBClassifier(learning_rate = 0.2, max_depth = 10)
clf_logistic = LogisticRegression(solver='lbfgs')

names = ["Xboost", "logmodel"]
preds_proba_ = pd.DataFrame(y_test.values, columns=["Actual"], index=y_test.index)
preds_proba = preds_proba_.merge(credit2['loan_amnt'],
                left_index=True, right_index=True )
preds_proba["loss_given_default"] = 1.0

# Store the average loan amount
avg_loan = np.mean(preds_proba["loan_amnt"])

fig, ax = plt.subplots()
for i, model in enumerate([gbt, clf_logistic]):

    # instantiate the model and fit
    clf = model.fit(X_train, np.ravel(y_train))

    # Predict with a model
    preds_proba[names[i]] = clf.predict_proba(X_test)[:,1]

    threshold, bad_rate, accept_num, loanTotal, losses, losses2 = [], [], [], [], [], []

    # compute threshold and bad rates
    for indx, r in enumerate(strategyTable["Accept_rate"].values):
        # Calculate the threshold for a 85% acceptance rate
        thres = np.quantile(preds_proba[names[i]], r).round(3)
        threshold.append(thres)

        # Apply acceptance rate threshold
        preds_proba[f"{names[i]}_rate"] = preds_proba[names[i]].apply(lambda x: 1 if x > thres else 0)

        # Create a subset of only accepted loans
        accepted_loans = preds_proba[preds_proba[f"{names[i]}_rate"] == 0]

        if accepted_loans.empty:
            accept_num.append(0.0)
            loanTotal.append(0.0)
            bad_rate.append(0.0)
            losses.append(0.0)
            losses2.append(0.0)

        else:
            accepted_loans.loc[:, ["impacttt"]] = accepted_loans[['Actual', 'loan_amnt']].apply(lambda x: 
                        -x[1] if x[0] == 1 else x[1], axis=1)  

            accept_num.append(accepted_loans.shape[0])
            loanTotal.append(accepted_loans["impacttt"].values.sum())

            losses2.append((accepted_loans[names[i]] * accepted_loans["loss_given_default"] * accepted_loans['impacttt']).sum())

            # Calculate the bad rate
            badrate = round(np.mean(accepted_loans['Actual'] == 1), 3)
            bad_rate.append(badrate)

            # calulate expected loss
            loss_df = accepted_loans[accepted_loans['Actual'] == 1]
            losses.append((loss_df[names[i]] * loss_df["loss_given_default"] * loss_df['loan_amnt']).sum())

    strategyTable[f"{names[i]}_Threshold"] = threshold   
    strategyTable[f"{names[i]}_Bad_Rate"] = bad_rate
    strategyTable[f"{names[i]}_TotalNum"] = accept_num 
    strategyTable[f"{names[i]}_TotalAmt"] = loanTotal
    strategyTable[f"{names[i]}_Expected Value"] = losses
    strategyTable[f"{names[i]}_Expected Value2"] = losses2

print(strategyTable, strategyTable.columns, **sp)

col = ['Accept_rate', 'Xboost_Threshold', 'Xboost_Bad_Rate', 
        'logmodel_Threshold', 'logmodel_Bad_Rate']

strategyTable[col].boxplot()
plt.show()

showlist = ["Expected Value", "Expected Value2", "Bad_Rate"]

# Plot the strategy curve bad rate
for i, val in enumerate(showlist):
    plt.plot(strategyTable["Accept_rate"], strategyTable[f"Xboost_{val}"],  label = "XGBoost Model")
    plt.plot(strategyTable["Accept_rate"], strategyTable[f"logmodel_{val}"], label = "Logistic Model")
    plt.xlabel('Acceptance Rate')
    plt.ylabel(f'{val}')
    plt.title(f'Acceptance and {val}')
    plt.legend()
    plt.show()

# Print the row with the max estimated value
for i in range(2):
    print(f"This is for {names[i]}")
    dd = strategyTable[[f"{names[i]}_Expected Value"]].idxmin()
    print(strategyTable.loc[dd, :])
    dd = strategyTable[[f"{names[i]}_TotalAmt"]].idxmax()
    print(strategyTable.loc[dd, :])
    dd = strategyTable[[f"{names[i]}_Expected Value2"]].idxmax()
    print(strategyTable.loc[dd, :], **sp)
    