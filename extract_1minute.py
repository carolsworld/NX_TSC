import pandas as pd
from pathlib import Path
from datetime import datetime

# File path
input_file = Path(r"C:\Users\ly-lo\Documents\Step 3_OPC_Data_20250413\opcua_csv\combined_opcua_dataset_instance1-60.csv")
output_file = input_file.parent / "opcua_instance1-60_sliced_1min.csv"

# Load CSV
df = pd.read_csv(input_file, low_memory=False)  # Helps avoid dtype inference errors
df['ts'] = pd.to_datetime(df['ts'], errors='coerce')  # Parse timestamp safely

# Ensure identifier is numeric (optional, for consistency in later steps)
if 'identifier' in df.columns:
    df['identifier'] = pd.to_numeric(df['identifier'], errors='coerce')

# Drop rows with NaT in timestamp (invalid or missing time values)
df = df.dropna(subset=['ts'])

# Output container
filtered_df = pd.DataFrame()

# Group by instance and filter to 1 minute window
for instance_id in df['instance'].dropna().unique():
    instance_data = df[df['instance'] == instance_id].copy()
    instance_data = instance_data.sort_values('ts')

    if not instance_data.empty:
        # Special handling for instance 28
        if instance_id == 28:
            end_time = pd.to_datetime("2025-04-04 10:05:25")
        else:
            end_time = instance_data.iloc[-1]['ts']
        
        start_time = end_time - pd.Timedelta(minutes=1)
        sliced_data = instance_data[(instance_data['ts'] >= start_time) & (instance_data['ts'] < end_time)]
        filtered_df = pd.concat([filtered_df, sliced_data], ignore_index=True)

# Save output
filtered_df.to_csv(output_file, index=False)
print(f"Saved 1-minute slice for each instance:\n{output_file}")