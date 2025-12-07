# Preprocessing functions

import pandas as pd

"""
Exclude Countries from DF with Missing Values Threshold >= 50%
"""
THRESHOLD = 50
def exclude_countries_high_missing_values(merged_df) -> pd.DataFrame:
    
    all_missing_values = merged_df.isnull().groupby(merged_df["Entity"]).sum()
    # get sum of values per country for 9 main potential features: 
    values_count_per_country = merged_df.groupby(merged_df["Entity"]).size().iloc[0] * 9
    
    all_missing_values["total_missing"] = all_missing_values.sum(axis=1)    #total missing values
    all_missing_values["total_missing_%"] = round((all_missing_values["total_missing"] / values_count_per_country) * 100, 2)  #total missing values %

    top_missing_countries = all_missing_values.sort_values(ascending=False, by="total_missing_%")
    exclude_countries = top_missing_countries[top_missing_countries["total_missing_%"] >= THRESHOLD]

    filtered_df_01 = merged_df[~merged_df["Entity"].isin(exclude_countries.index.tolist())].copy()

    #print("NEW FILTERED DF", filtered_df_01)
    return filtered_df_01


"""
(REMOVE)
Handle missing values #2: add missing values indicator (0 or 1)
Make only for columns that have null values
0 = not missing & 1 = missing
"""
"""
def missing_values_indicator(df) -> pd.DataFrame:
    
    missing_indicators_df = df.copy()
    
    for column in missing_indicators_df.columns:
        if missing_indicators_df[column].isna().sum() > 0:
            missing_indicators_df[column+"_missing"] = missing_indicators_df[column].isna().astype(int)
    print("DF with missing indicators", missing_indicators_df)
    return missing_indicators_df
"""