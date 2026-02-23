# Pipeline from Data Loading to Model ("Production Ready")
#----------------------------------------------------------------------
# model_pipeline.py
#
# Data Preparation: Get main, cleaned dataset from data_cleaning.py & config.py
#
# Model Pipeline: 
# Extract numeric, categorical features as "X", country (Entity) as group, and target variable as "y"
# GroupShuffleSplit Train-Testset, Preprocessing Pipeline from data_preprocessing.py
# Fit and save model
#----------------------------------------------------------------------


# ----------------------------------
# IMPORTS
#-----------------------------------

import pandas as pd
import numpy as np

from sklearn.model_selection import GroupShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.compose import TransformedTargetRegressor

from sklearn.linear_model import QuantileRegressor

import joblib

from data_preprocessing import preprocessing_pipeline

import config

# ----------------------------------
# Train/Test Split
#-----------------------------------
gs_split = GroupShuffleSplit(n_splits=1, train_size=0.8, test_size=0.2, random_state=99)
train_index, test_index = next(gs_split.split(config.X, config.y, config.group))

X_train, X_test = config.X.iloc[train_index], config.X.iloc[test_index]
y_train, y_test = config.y.iloc[train_index], config.y.iloc[test_index]
group_train = config.group.iloc[train_index]
group_test  = config.group.iloc[test_index]

#Save Trainset and Testset as csv
X_train.assign(Entity=group_train).to_csv("../00_data/2_split/X_train_df.csv", index=False)
X_test.assign(Entity=group_test).to_csv("../00_data/2_split/X_test_df.csv", index=False)

# ----------------------------------
# Preprocessing Pipeline
#-----------------------------------
pre_pipe = preprocessing_pipeline()

# ----------------------------------
# Define 3 Quantiles
#-----------------------------------
qr_quantiles = [0.25, 0.5, 0.75]

# ----------------------------------
# Loop Quantiles Fit & Save Q-Models
#-----------------------------------
print("Start Final Model Pipeline & Fit Pipeline")
for q in qr_quantiles:
    
        
    model_pipe = Pipeline([
        ("preprocess", pre_pipe),
        ("model", QuantileRegressor(
                quantile=q,
                alpha=0.01
        ))
    ])
        
    model_pipe.fit(X_train, y_train)

    y_pred_holdout = model_pipe.predict(X_test)
    residuen = y_test - y_pred_holdout
    shift = np.quantile(residuen, q)
    #print(shift)
        
    model_pipe.fit(config.X, config.y)
        
    joblib.dump(model_pipe, f"../04_models/quantile_{q}.pkl")
    #joblib.dump(shift, f"../04_models/shift_quant{q}.pkl")

    print(f"Quantile {q} model saved")