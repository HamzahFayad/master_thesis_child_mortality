# Pipeline from Data Loading to Model Training
#----------------------------------------------------------------------
#model_pipeline.py
#
# Data Preparation: Get main, cleaned dataset from data_cleaning.py & data_preprocessing.py
#
# Model Pipeline: 
# Extract numeric, categorical features as "X", country (Entity) as group, and target variable as "y"
# GroupShuffleSplit Train-Testset, crossvalidate (GroupKFold) Pipeline with GridSearchCV for 3 models
#----------------------------------------------------------------------


# ----------------------------------
# IMPORTS
#-----------------------------------

import pandas as pd
import numpy as np

from sklearn.model_selection import GroupShuffleSplit, GroupKFold, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

from sklearn.preprocessing import RobustScaler, PowerTransformer, OneHotEncoder

from sklearn.impute import KNNImputer

from sklearn.cluster import KMeans

from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor

from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score

from data_cleaning import load_merge_raw_data
from data_preprocessing import exclude_countries_high_missing_values

#Data Path
DATA_PATH = "../00_data/0_raw/"

"""
Prepare datasets
@return main prepared dataframe to 
"""
def data_preparation():
    #STEP 1: Load & Merge DATASETS, EXCLUDE NON-COUNTRIES & LIMIT TO 6-YEAR PERIOD PER COUNTRY
    merged_df = load_merge_raw_data(DATA_PATH)
    #STEP 2: REMOVE COUNTRIES WITH HIGH AMOUNT OF MISSING VALUES (>=50%)
    df = exclude_countries_high_missing_values(merged_df)
    #print("Prepared Main Dataset:\n", df)
    return df

prepared_df = data_preparation()


# ----------------------------------
# VARIABLES: Features, Target, Group
#-----------------------------------

y = prepared_df["child_mortality_igme"]
X = prepared_df.drop(columns=["Code", "Entity", "Year", "child_mortality_igme"])
group = prepared_df["Entity"]

num_variables = X.drop(columns=["world_regions_wb"]).columns.to_list()
cat_variables = ["world_regions_wb"]

#print(X.columns)

# ----------------------------------
# Train/Test Split
#-----------------------------------
gs_split = GroupShuffleSplit(n_splits=1, train_size=0.8, test_size=0.2, random_state=99)
train_index, test_index = next(gs_split.split(X, y, group))

X_train, X_test = X.iloc[train_index], X.iloc[test_index]
y_train, y_test = y.iloc[train_index], y.iloc[test_index]
group_train = group.iloc[train_index]
group_test  = group.iloc[test_index]

#Save Trainset and Testset as csv
X_train.assign(Entity=group_train).to_csv("../00_data/2_split/X_train_df.csv", index=False)
X_test.assign(Entity=group_test).to_csv("../00_data/2_split/X_test_df.csv", index=False)

#X_train.to_csv("../00_data/2_split/X_train_df.csv", index=False)
#X_test.to_csv("../00_data/2_split/X_test_df.csv", index=False)