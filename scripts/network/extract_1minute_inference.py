import pandas as pd
from pathlib import Path
from zoneinfo import ZoneInfo  # Python 3.9+

# File paths
input_file = Path(r"C:\Users\ly-lo\Documents\20250509_All Steps\OT Network\20250509_Network_OPCUA_enriched_features.csv")
output_file_1 = Path(r"C:\Users\ly-lo\Documents\20250509_All Steps\OT Network\20250509_Network_OPCUA_enriched_features_instanced_file1.csv")
output_file_2 = Path(r"C:\Users\ly-lo\Documents\20250509_All Steps\OT Network\20250509_Network_OPCUA_enriched_features_instanced_file2.csv")

# Load and parse timestamp in UTC
df = pd.read_csv(input_file, low_memory=False)
df['ts'] = pd.to_datetime(df['ts'], errors='coerce')
df = df.dropna(subset=['ts'])

# --- Add UK local time column (for reference) ---
df['ts_uk'] = df['ts'].dt.tz_localize('UTC').dt.tz_convert('Europe/London')

# Round down to the nearest minute (UTC)
df['minute'] = df['ts'].dt.floor('min')

# --- Define explicit time ranges for both files ---
start_time_file1 = pd.to_datetime("2025-05-09 13:35:00")  # inclusive
end_time_file1 = pd.to_datetime("2025-05-09 14:54:00")    # inclusive

start_time_file2 = pd.to_datetime("2025-05-09 14:55:00")  # inclusive
end_time_file2 = df['minute'].max()  # optional: until the end of the data

# --- Filter and assign instances ---

# File 1: Instances 1–N
df_file1 = df[(df['minute'] >= start_time_file1) & (df['minute'] <= end_time_file1)].copy()
unique_minutes_1 = sorted(df_file1['minute'].unique())
instance_map_1 = {minute: i + 1 for i, minute in enumerate(unique_minutes_1)}
df_file1['instance'] = df_file1['minute'].map(instance_map_1)

# File 2: Instances continue from the next number
df_file2 = df[(df['minute'] >= start_time_file2) & (df['minute'] <= end_time_file2)].copy()
unique_minutes_2 = sorted(df_file2['minute'].unique())
instance_map_2 = {minute: i + len(instance_map_1) + 1 for i, minute in enumerate(unique_minutes_2)}
df_file2['instance'] = df_file2['minute'].map(instance_map_2)

# Drop helper column
df_file1.drop(columns=['minute'], inplace=True)
df_file2.drop(columns=['minute'], inplace=True)

# Export
df_file1.to_csv(output_file_1, index=False)
df_file2.to_csv(output_file_2, index=False)

print(f"File 1 saved: {output_file_1} ({df_file1['instance'].nunique()} instances)")
print(f"File 2 saved: {output_file_2} ({df_file2['instance'].nunique()} instances)")