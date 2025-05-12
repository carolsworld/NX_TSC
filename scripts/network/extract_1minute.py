import pandas as pd
from pathlib import Path

# File paths
input_file = Path(r"C:\Users\ly-lo\Documents\20250509_All Steps\OT Network\1. 60 enriched csv\combined_opcua_dataset_instance1-60.csv")
output_file = input_file.parent / "opcua_instance1-60_sliced_1min.csv"

# Load and parse timestamps
df = pd.read_csv(input_file, low_memory=False)
df['ts'] = pd.to_datetime(df['ts'], errors='coerce')
df = df.dropna(subset=['ts'])

# Convert identifier to numeric (optional but consistent)
if 'identifier' in df.columns:
    df['identifier'] = pd.to_numeric(df['identifier'], errors='coerce')

# Output container
filtered_df = pd.DataFrame()

# Slice 1 minute per instance
for instance_id in sorted(df['instance'].dropna().unique()):
    instance_data = df[df['instance'] == instance_id].copy()
    instance_data = instance_data.sort_values('ts')

    if not instance_data.empty:
        if instance_id == 28:
            # Special fixed end timestamp for instance 28
            end_time = pd.to_datetime("2025-04-04 10:05:25")
        else:
            end_time = instance_data.iloc[-1]['ts']

        start_time = end_time - pd.Timedelta(minutes=1)
        sliced_data = instance_data[(instance_data['ts'] >= start_time) & (instance_data['ts'] < end_time)]

        # Optional: filter out very short instances (less than 100 rows)
        if len(sliced_data) >= 100:
            filtered_df = pd.concat([filtered_df, sliced_data], ignore_index=True)
        else:
            print(f"[!] Instance {instance_id} has only {len(sliced_data)} rows — skipped.")

# Save
filtered_df.to_csv(output_file, index=False)
print(f"[✓] Trimmed training data saved with {filtered_df['instance'].nunique()} valid instances:\n{output_file}")