import pandas as pd
from pathlib import Path

# Input enriched CSV
input_path = Path(r"C:\Users\ly-lo\Documents\20250509_All Steps\OT Network\20250509_Network_OPCUA_enriched.csv")

# Output path (same folder or different if you prefer)
output_path = Path(r"C:\Users\ly-lo\Documents\20250509_All Steps\OT Network\20250509_Network_OPCUA_enriched_features.csv")

# Define columns to retain
selected_columns = [
    'ts', 'uid', 'id.orig_h', 'id.orig_p', 'id.resp_h', 'id.resp_p',
    'is_orig', 'opcua_link_id', 'is_final', 'msg_size', 'identifier',
    'node_id_string'
]

# Load, filter, and save
df = pd.read_csv(input_path)

missing = [col for col in selected_columns if col not in df.columns]
if missing:
    raise ValueError(f"Missing columns in input file: {missing}")

df = df[selected_columns]
df.to_csv(output_path, index=False)

print(f"Filtered CSV saved to: {output_path}")