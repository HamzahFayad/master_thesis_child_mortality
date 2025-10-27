# Preprocessing functions

import pandas as pd

# Exclude Countries from DF with Missing Values Threshold >= 50%
THRESHOLD = 50
def exclude_countries_high_missing_values(merged_df) -> pd.DataFrame:
    
    all_missing_values = merged_df.isnull().groupby(level=0).sum()
    all_missing_values["total_missing"] = all_missing_values.sum(axis=1)    #total missing values
    all_missing_values["total_missing_%"] = round((all_missing_values["total_missing"] / 54) * 100, 2)  #total missing values %

    top_missing_countries = all_missing_values.sort_values(ascending=False, by="total_missing_%")
    exclude_countries = top_missing_countries[top_missing_countries["total_missing_%"] >= THRESHOLD]

    filtered_df_01 = merged_df[~merged_df.index.get_level_values(0).isin(exclude_countries.index.tolist())].copy()

    #print("NEW FILTERED DF", filtered_df_01)
    return filtered_df_01


"""
Handle missing values for column vaccination_coverage (6 NaNs for Nicaragua (NIC))
"""
def handle_missing_vaccination(filtered_df_01) -> pd.DataFrame:
    COUNTRY_CODE = "NIC"
    COUNTRY_NAME = "Nicaragua"
    world_regions = pd.read_csv("./00_data/0_raw/world-regions-worldbank.csv")
    #calculate median
    return processed_df_01