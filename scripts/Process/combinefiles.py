import os
import pandas as pd
import re

# Input/output
folder = 'C:/Users/babya/Desktop/NX_Data/Step 1. Standardized'
output_file = os.path.join(folder, 'NX_data.csv')

# Natural sorting by instance number
def extract_instance_number(filename):
    match = re.search(r'Instance_(\d+)_standardised_fixed\.csv', filename)
    return int(match.group(1)) if match else float('inf')

# List and sort files
files = [f for f in os.listdir(folder) if f.endswith('_standardised_fixed.csv')]
files_sorted = sorted(files, key=extract_instance_number)

# Combine with only one header
combined_df = pd.read_csv(os.path.join(folder, files_sorted[0]))  # Read first with header

for f in files_sorted[1:]:
    df = pd.read_csv(os.path.join(folder, f))
    combined_df = pd.concat([combined_df, df], ignore_index=True)

# Save with single header
combined_df.to_csv(output_file, index=False)
print(f"Combined CSV created: {output_file}")

for f in files_sorted:
    df = pd.read_csv(os.path.join(folder, f), nrows=1)
    print(f"{f}: {list(df.columns)}")