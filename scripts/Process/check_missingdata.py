import pandas as pd

combined_path = "C:/Users/babya/Desktop/NX_Data/Step 1. Standardized/NX_data.csv"
df = pd.read_csv(combined_path)

# Overview of missing values
missing_summary = df.isnull().sum()
print("Missing values summary:\n", missing_summary[missing_summary > 0])