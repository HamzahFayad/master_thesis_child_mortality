#----------------------------------------------------------------------
# data_preprocessing.py
#
# Define entire preprocessing ML pipeline
#----------------------------------------------------------------------


import pandas as pd
import numpy as np

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import RobustScaler, PowerTransformer, OneHotEncoder, FunctionTransformer
from sklearn.impute import KNNImputer, SimpleImputer
import config


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
    
# ----------------------------------
# Preprocessing Pipeline Steps
#-----------------------------------
def preprocessing_pipeline():
    
    print(f"Initialize Preprocessing: Imputing, Transforming, Scaling, OHE...")

    # HEALTH/GDP RATIO FUNCTRANSFORMER
    ratio_feature = FunctionTransformer(
        func = ratio_health_gdp, 
        validate = False, 
        feature_names_out=passthrough_featurenames
        )

    # IMPUTE AND TRANSFORM NUMERIC VARIABLES
    impute_transform = ColumnTransformer([
        
        ("pre_rightskewed", Pipeline([
            ("knn_impute1", KNNImputer(n_neighbors=5, weights="distance")),
            ("log_transform", FunctionTransformer(np.log1p, feature_names_out="one-to-one"))
        ]), config.right_skewed_cols),
        
        ("pre_leftskewed", Pipeline([
            ("knn_impute2", KNNImputer(n_neighbors=5, weights="distance")),
            ("power_transform", PowerTransformer(method="yeo-johnson"))
        ]), config.left_skewed_cols),
        
        ("pre_normal", Pipeline([
            ("knn_impute3", KNNImputer(n_neighbors=5, weights="distance")),
        ]), config.normal_cols),
            
    ], verbose_feature_names_out=False, remainder='passthrough').set_output(transform="pandas")

    # CREATE A RATIO COLUMN  
    ratio_he_gdp = ColumnTransformer([
        
        ("health_gdp_ratio", Pipeline([
            ("health_gdp_ratio", ratio_feature),
        ]), [config.col_gdp, config.col_healthspending])
        
    ], verbose_feature_names_out=False, remainder="passthrough").set_output(transform="pandas")

    # ONE HOT ENCODE CATEGORIC VARIABLES
    ohe_cats = Pipeline(steps=[
        ("impute", SimpleImputer(strategy="constant", fill_value="missing")),
        ("ohe", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
    ])

    # SCALE NUM VARIABLES & USE OHE ON CAT VARIABLES
    scale_ohe_step = ColumnTransformer([
        
        ("drop_num_cols", "drop", [config.col_gdp, config.col_healthspending]),
        ("scale_nums", RobustScaler(), config.rest_nums + ["healthspending_gdp_ratio"]),
        ("ohe_cats", ohe_cats, [config.col_regions, config.col_incomegroup]),
        
    ], verbose_feature_names_out=False, remainder="passthrough").set_output(transform="pandas")

    # END PIPELINE TO COMBINE ALL PREPROCESSING STEPS
    end_pipe = Pipeline([
        
        ("prep_nums", impute_transform),
        ("ratio_feature", ratio_he_gdp),
        ("scale_ohe", scale_ohe_step),
        ("final_impute", KNNImputer(n_neighbors=5, weights="distance"))
        
    ])
    
    print(f"Preprocessing finished...")
    
    return end_pipe