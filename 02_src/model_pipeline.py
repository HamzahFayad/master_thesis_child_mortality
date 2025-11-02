# Pipeline from Data Loading to Model Training

#import pandas as pd

from data_loading import load_merge_raw_data
from data_preprocessing import exclude_countries_high_missing_values
#Variables
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
    df = df.reset_index()
    print(df)

    
    
data_preparation()