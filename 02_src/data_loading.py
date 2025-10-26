# Step A - load raw Data + merge all data with u5mr as base + filter 6 year period + scale up label to 1000

import pandas as pd
import os

#get all data files & sort
PATH = "../00_data/0_raw/"
all_files = [f for f in os.listdir(PATH)]
sorted_files = sorted(os.listdir(PATH))
#print(sorted_files)

#u5mr file at first position (base)
label_file = sorted_files.pop(1)
sorted_files.insert(0, label_file)

#list of non-countries to exclude in 'Entity' column
EXCLUDE_NO_COUNTRIES = ["Africa", "Asia", "Europe", "European Union (27)", "High-income countries", "Low-income countries", "Lower-middle-income countries", 
                      "North America", "Oceania", "South America", "Upper-middle-income countries", "World"]

#create column names from files
def new_col_names(name):
    return os.path.basename(name).split('.')[0].replace('-', '_')

#limit df to 6 year period 2013-2018
FROM_YEAR = 2013
TO_YEAR = 2018
def limit_period(df) -> pd.DataFrame:
    df = df[(df.index.get_level_values(2) >= FROM_YEAR) & (df.index.get_level_values(2) <= TO_YEAR)]
    return df

"""
load raw data, join columns, 
exclude non-countries, 
set Multi-Index and merge all 10 df
scale U5MR up to 1000
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
            big_df = limit_period(big_df)
    
    big_df["child_mortality_igme"] = big_df["child_mortality_igme"] * 10
    big_df = big_df.reset_index(level=0)
    print(big_df)  
    return big_df




load_merge_raw_data(PATH)


