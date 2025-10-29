# Preprocessing functions

import pandas as pd

"""
Exclude Countries from DF with Missing Values Threshold >= 50%
"""
THRESHOLD = 50
def exclude_countries_high_missing_values(merged_df) -> pd.DataFrame:
    
    all_missing_values = merged_df.isnull().groupby(level=0).sum()
    # get sum of values per country for 9 main potential features: 
    values_count_per_country = merged_df.groupby(level=0).size().iloc[0] * 9
    
    all_missing_values["total_missing"] = all_missing_values.sum(axis=1)    #total missing values
    all_missing_values["total_missing_%"] = round((all_missing_values["total_missing"] / values_count_per_country) * 100, 2)  #total missing values %

    top_missing_countries = all_missing_values.sort_values(ascending=False, by="total_missing_%")
    exclude_countries = top_missing_countries[top_missing_countries["total_missing_%"] >= THRESHOLD]

    filtered_df_01 = merged_df[~merged_df.index.get_level_values(0).isin(exclude_countries.index.tolist())].copy()

    print("NEW FILTERED DF", filtered_df_01)
    return filtered_df_01


"""
Handle missing values #2: add missing values indicator (0 or 1)
Make only for columns that have null values
0 = not missing & 1 = missing
"""
def missing_values_indicator(filtered_df_01) -> pd.DataFrame:
    
    missing_indicators_df = filtered_df_01.copy()
    
    for column in missing_indicators_df.columns:
        if missing_indicators_df[column].isna().sum() > 0:
            missing_indicators_df[column+"_missing"] = missing_indicators_df[column].isna().astype(int)
    print("DF with missing indicators", missing_indicators_df)
    return missing_indicators_df