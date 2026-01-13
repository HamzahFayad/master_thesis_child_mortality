# Pipeline from Data Loading to Model Training
#----------------------------------------------------------------------
#model_pipeline.py
#
# Data Preparation: Get main, cleaned dataset from data_cleaning.py & data_preprocessing.py
#
# Model Pipeline: 
# Extract numeric, categorical features as "X", country (Entity) as group, and target variable as "y"
# GroupShuffleSplit Train-Testset, Pipeline
#----------------------------------------------------------------------


# ----------------------------------
# IMPORTS
#-----------------------------------

import pandas as pd
import numpy as np

from sklearn.model_selection import GroupShuffleSplit, GroupKFold
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer, TransformedTargetRegressor

from sklearn.preprocessing import RobustScaler, PowerTransformer, OneHotEncoder, FunctionTransformer

from sklearn.impute import KNNImputer, SimpleImputer

#from sklearn.cluster import KMeans

from sklearn.linear_model import QuantileRegressor

import joblib
#from joblib import dump


from data_cleaning import load_merge_raw_data
from data_preprocessing import exclude_countries_high_missing_values

#Data Path
DATA_PATH = "../00_data/0_raw/"

"""
PREPARE DATASETS
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

num_variables = X.drop(columns=["world_regions_wb", "world_income_group"]).columns.to_list()
cat_variables = ["world_regions_wb", "world_income_group"]

normal_cols = ["years_of_schooling", "share_of_population_urban"]
left_skewed_cols = ["vaccination_coverage_who_unicef"]
norm_left = normal_cols + left_skewed_cols

right_skewed_cols = num_variables.copy() 
for el in norm_left:
    if el in right_skewed_cols:
        right_skewed_cols.remove(el)
        
#all numeric variables
all_numeric_cols = right_skewed_cols + left_skewed_cols + normal_cols

#categoric variables
col_country = "Entity"             
col_regions = "world_regions_wb"  
col_incomegroup = "world_income_group"

#cols to combine
col_healthspending = "annual_healthcare_expenditure_per_capita"
col_gdp = "gdp_per_capita_worldbank"

rest_nums = num_variables[2:]
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


# ----------------------------------
# create ratio variable from healthspending & gdp
# @return FunctionTransformer
#-----------------------------------
def passthrough_featurenames(transformer, input_features=None):
    return ["gdp_per_capita_worldbank", 
            "annual_healthcare_expenditure_per_capita", 
            "healthspending_gdp_ratio"]

def ratio_health_gdp(X):
    X = X.copy()
    X["healthspending_gdp_ratio"] = (
        X["annual_healthcare_expenditure_per_capita"] - 
        X["gdp_per_capita_worldbank"]
    )
    return X

ratio_feature = FunctionTransformer(
    func = ratio_health_gdp, 
    validate = False, 
    feature_names_out=passthrough_featurenames
    )

# ----------------------------------
# Preprocessing Pipeline Steps
#-----------------------------------

# IMPUTE AND TRANSFORM NUMERIC VARIABLES
impute_transform = ColumnTransformer([
    
    ("pre_rightskewed", Pipeline([
        ("knn_impute1", KNNImputer(n_neighbors=5, weights="distance")),
        ("log_transform", FunctionTransformer(np.log1p, feature_names_out="one-to-one"))
    ]), right_skewed_cols),
    
    ("pre_leftskewed", Pipeline([
        ("knn_impute2", KNNImputer(n_neighbors=5, weights="distance")),
        ("power_transform", PowerTransformer(method="yeo-johnson"))
    ]), left_skewed_cols),
    
    ("pre_normal", Pipeline([
        ("knn_impute3", KNNImputer(n_neighbors=5, weights="distance")),
    ]), normal_cols),
          
], verbose_feature_names_out=False, remainder='passthrough').set_output(transform="pandas")

# CREATE A RATIO COLUMN  
ratio_he_gdp = ColumnTransformer([
    
    ("health_gdp_ratio", Pipeline([
        ("health_gdp_ratio", ratio_feature),
    ]), [col_gdp, col_healthspending])
    
], verbose_feature_names_out=False, remainder="passthrough").set_output(transform="pandas")

# ONE HOT ENCODE CATEGORIC VARIABLES
ohe_cats = Pipeline(steps=[
    ("impute", SimpleImputer(strategy="constant", fill_value="missing")),
    ("ohe", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
])

# SCALE NUM VARIABLES & USE OHE ON CAT VARIABLES
scale_ohe_step = ColumnTransformer([
    
    ("drop_num_cols", "drop", [col_gdp, col_healthspending]),
    ("scale_nums", RobustScaler(), rest_nums + ["healthspending_gdp_ratio"]),
    ("ohe_cats", ohe_cats, [col_regions, col_incomegroup]),
    #("drop_country", "drop", [col_country])
    
], verbose_feature_names_out=False, remainder="passthrough").set_output(transform="pandas")

# END PIPELINE TO COMBINE ALL PREPROCESSING STEPS
end_pipe = Pipeline([
    
    ("prep_nums", impute_transform),
    ("ratio_feature", ratio_he_gdp),
    ("scale_ohe", scale_ohe_step),
    ("final_impute", KNNImputer(n_neighbors=5, weights="distance"))
    
])


qr_quantiles = [0.25, 0.5, 0.75]
#qr_models = {}

for q in qr_quantiles:
    
    model_pipe = Pipeline([
        ("preprocess", end_pipe),
        ("model", QuantileRegressor(
                quantile=q,
                alpha=0.01
        ))
    ])
    
    qr_pipeline = TransformedTargetRegressor(
        regressor=model_pipe,
        func=np.log1p,
        inverse_func=np.expm1
    )
    
    qr_pipeline.fit(X_train, y_train)
    #qr_pipeline.fit(X, y)

    y_pred_holdout = qr_pipeline.predict(X_test)
    residuen = y_test - y_pred_holdout
    shift = np.quantile(residuen, q)
    #print(shift)
    
    qr_pipeline.fit(X, y)
    
    joblib.dump(qr_pipeline, f"../04_models/quantile_{q}.pkl")
    #joblib.dump(qr_pipeline, f"../04_models/quant_{q}.pkl")
    joblib.dump(shift, f"../04_models/shift_quant{q}.pkl")

#print("Quantile models saved")