# Preprocessing functions

import pandas as pd

# Exclude Countries from DF with Missing Values Threshold >= 50%
THRESHOLD = 50
def exclude_countries_high_missing_values(merged_df, total_values) -> pd.DataFrame:
    
    all_missing_values = merged_df.isnull().groupby(level=0).sum()
    all_missing_values["total_missing"] = all_missing_values.sum(axis=1)    #total missing values
    all_missing_values["total_missing_%"] = round((all_missing_values["total_missing"] / total_values) * 100, 2)  #total missing values %

    top_missing_countries = all_missing_values.sort_values(ascending=False, by="total_missing_%")
    exclude_countries = top_missing_countries[top_missing_countries["total_missing_%"] >= THRESHOLD]

    filtered_df_01 = merged_df[~merged_df.index.get_level_values(0).isin(exclude_countries.index.tolist())].copy()

    #print("NEW FILTERED DF", filtered_df_01)
    return filtered_df_01


"""
Handle missing values for column vaccination_coverage (6 NaNs for Nicaragua (NIC))
"""

# def handle_missing_vaccination(filtered_df_01) -> pd.DataFrame:
#     WORLDBANK_REG = "../00_data/1_interim/world-regions-worldbank.csv"
#     COUNTRY_CODE = "NIC"
#     COUNTRY_NAME = "Nicaragua"
#     REGION = "Latin America and Caribbean (WB)"
#     COL = "vaccination_coverage_who_unicef"
    
#     world_regions = pd.read_csv(WORLDBANK_REG)
#     country_groups = world_regions.loc[:, ["Code", "World regions according to WB"]]
    
#     processed_df_01 = filtered_df_01.copy()
#     processed_df_01 = processed_df_01.reset_index()
#     processed_df_01 = processed_df_01.merge(country_groups, on=['Code'], how="left")
#     processed_df_01 = processed_df_01.set_index(["Code", "Year"])
    
#     median_values = processed_df_01.groupby(["World regions according to WB"])[COL].median()
#     median_val = median_values.loc[REGION]
    
#     filtered_df_01.loc[filtered_df_01["Entity"] == COUNTRY_NAME, COL] = median_val

#     print("fill vaccination missing values: \n", filtered_df_01, filtered_df_01.isna().sum())
#     return filtered_df_01