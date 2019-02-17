#!/usr/bin/env python
import os 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('ggplot')


def show_result(dataframe1, dataframe2):
    namelist = {'Female': dataframe1, 'Male': dataframe2}
    for key, value in namelist.items():
        name = list(value.columns)
        value[key] = value[name[0]]
        value.drop(name[0], axis=1, inplace=True)
        value.reset_index(inplace=True)

    df5 = dataframe1.merge(dataframe2, left_on='index', right_on='index')
    print(df5.head())


path = "C:\\Users\\Jose\\Desktop\\TimerSeriesAnalysis\\police_nj\\"
os.chdir(path)

wy = pd.read_csv('cleaned_wy.csv', parse_dates=True, index_col='stop_datetime')
print(wy.head())
print(wy.info())

# Count the unique values in 'violation'
# print(len(wy.violation.unique()))
print(wy.violation.value_counts())

# # Express the counts as proportions
print(wy.violation.value_counts(normalize=True))


# ####################### Question1: is there gender difference or effect on violation committed
# Create a DataFrame of female drivers
female = wy[wy.driver_gender == 'F']

# Create a DataFrame of male drivers
male = wy[wy.driver_gender == 'M']

# Compute the violations by female drivers (as proportions)
femaletab = pd.DataFrame(female.violation.value_counts(normalize=True))

# Compute the violations by male drivers (as proportions)
maletab = pd.DataFrame(male.violation.value_counts(normalize=True))

# show the table of result
show_result(femaletab, maletab)



# question 2: Does gender and race affect stops by the police for speeding
# Create a DataFrame of female drivers stopped for speeding
female_and_speeding = wy[(wy.driver_gender == 'F') & (wy.violation == 'Speeding')]

# Create a DataFrame of male drivers stopped for speeding
male_and_speeding = wy[(wy.driver_gender == 'M') & (wy.violation == 'Speeding')]

# Compute the stop outcomes for female drivers (as proportions)
females22 = pd.DataFrame(female_and_speeding.driver_race.value_counts(normalize=True))

# Compute the stop outcomes for male drivers (as proportions)
males22 = pd.DataFrame(male_and_speeding.driver_race.value_counts(normalize=True))

# show the table of result
show_result(females22, males22)




################ Question 3: Does gender affect drug related stops by the police
# Compute the drug related stops by female drivers (as proportions)
femaled = pd.DataFrame(female.drugs_related_stop.value_counts(normalize=True))

# Compute the drug related stops by male drivers (as proportions)
maled = pd.DataFrame(male.drugs_related_stop.value_counts(normalize=True))

show_result(femaled, maled)