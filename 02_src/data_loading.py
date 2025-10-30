# Step A - load raw Data + merge all data with u5mr as base + filter 6 year period + scale up label to 1000

#Imports
import pandas as pd
import os
from datetime import date

#get all data files & sort
PATH = "../00_data/0_raw/"
all_files = [f for f in os.listdir(PATH)]
sorted_files = sorted(os.listdir(PATH))
#print(sorted_files)

#u5mr file at first position (base for merging)
label_file = sorted_files.pop(1)
sorted_files.insert(0, label_file)

#list of non-countries to exclude in 'Entity' column
EXCLUDE_NO_COUNTRIES = ["Africa", "Asia", "Europe", "European Union (27)", "High-income countries", "Low-income countries", "Lower-middle-income countries", 
                      "North America", "Oceania", "South America", "Upper-middle-income countries", "World"]

#create column names from files
def new_col_names(name):
    return os.path.basename(name).split('.')[0].replace('-', '_')

"""
Limit DF to 6 year period:
Loop in 6 year periods and append to list as tuples
extract tuple of minimum null count, 6 year period with least NaN values
@return filtered df
"""
def get_years_period(df):
    nulls_list = []
    null_count = 0
    year_idx = df.index.get_level_values(2)
    
    for begin in range(2000, year_idx.max() - 4):
        end = begin + 5
        df_six_years = df[(year_idx >= begin) & (year_idx <= end)]
        null_count = df_six_years.isna().sum().sum()
        nulls_list.append((begin, end, null_count)) #list of tuple (begin, end, null_values count) 
        #print(f"From {begin} - {end}, NaN values count: {null_count}")
        
    # get the minimum NaN value
    found_period = min(nulls_list, key=lambda n: n[2])
    df = df[(df.index.get_level_values(2) >= found_period[0]) & (df.index.get_level_values(2) <= found_period[1])]

    return df



# def limit_period(df) -> pd.DataFrame:
#     df = df[(df.index.get_level_values(2) >= 2013) & (df.index.get_level_values(2) <= 2018)]
#     return df

"""
Load and Merge all CSV files:
load raw data, join columns, 
exclude non-countries, 
set Multi-Index and merge all 10 df
scale U5MR up to 1000
@return merged, limited df
"""
def load_merge_raw_data(PATH) -> pd.DataFrame:
    big_df = None
    joins = ['Entity', 'Code', 'Year']
    
    for name in sorted_files:
        cols_names = new_col_names(name)
        
        df = pd.read_csv(os.path.join(PATH, name), usecols=[0, 1, 2, 3])
        df.columns = joins + [cols_names]
        
        df = df[~df['Entity'].isin(EXCLUDE_NO_COUNTRIES)]
    
        df = df.set_index(joins) 

        if big_df is None:
            big_df = df.copy() 
        else: 
            big_df = big_df.merge(
                df, 
                left_index=True, 
                right_index=True, 
                how='left' 
            )
    # get six years period with least NaNs and limit big_df
    big_df = get_years_period(big_df)
    #big_df = limit_period(big_df)

    big_df["child_mortality_igme"] = big_df["child_mortality_igme"] * 10
    big_df = big_df.reset_index(level=0)
    print(big_df)  
    return big_df




load_merge_raw_data(PATH)


