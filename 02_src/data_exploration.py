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