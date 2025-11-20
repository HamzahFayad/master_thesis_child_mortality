import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
# Reusable Functions - Data Exploration

"""
Count missing values for each column in a df
absolute count and percentage count
"""
def count_missing_values(df):
    print(f"DataFrame has {df.isna().sum().sum()} null values in total.\n")
    null_count = df.isna().sum()
    null_count_perc = round((null_count / len(df)) * 100, 2)
    print(f"Missing Values - count for each column:\n\n{null_count}\n\nPercentage of Missing values:\n\n{null_count_perc}")
    

"""
Plot scatterplots to show relationships between label and features
3 cols for comparisons
"""
def scatterplots(df, features, cols_num):
    fig, axs = plt.subplots(ncols=cols_num, figsize=(18, 6))
    for id, a in enumerate(axs):
        sns.scatterplot(data=df, x="child_mortality_igme", y=features[id], hue=features[id], 
                        size=features[id], sizes=(25, 100), ax=axs[id])
    plt.show()
    
"""
Plot histograms of numeric variables
"""    
def histograms(df):
    df.hist(figsize=(14,8))
    plt.tight_layout()
    plt.show()
