import pandas as pd

# Load your single CSV
df = pd.read_csv("/home/uwe/20250502 Network/zeek_log_ot/20250502_opcua_binary_localtime.csv", low_memory=False)

# Keep only relevant columns
selected_columns = [
    'ts', 'uid', 'id.orig_h', 'id.orig_p', 'id.resp_h', 'id.resp_p',
    'is_orig', 'opcua_link_id', 'is_final', 'msg_size', 'identifier'
]
df = df[selected_columns]

# Convert timestamp to appropriate format
df['ts'] = pd.to_datetime(df['ts'], errors='coerce')

# Use source port to distinguish between HMI, UA Expert or PLC (automated activity)
df['id.orig_p'] = pd.to_numeric(df['id.orig_p'], errors='coerce')

#  Binary encode for message initiator (OPC UA client / message request = 1; OPC UA server / message responder = 0)
df['is_orig'] = df['is_orig'].astype(str).str.strip().str.upper().map({'T': 1, 'F': 0})

#  Binary encode for message status (Complete message = 1; Incomplete message = 0)
df['is_final'] = df['is_final'].astype(str).str.strip().str.upper().map({'T': 1, 'F': 0})

# Convert identifier to numeric, drop invalid rows
df['identifier'] = pd.to_numeric(df['identifier'], errors='coerce')
df.dropna(subset=['identifier'], inplace=True)

# Ensure msg_size is numeric
df['msg_size'] = pd.to_numeric(df['msg_size'], errors='coerce')

# Add semantic flags - in OPC UA, identifier #673 is write requests
df['is_WriteOps'] = (df['identifier'] == 673).astype(int)

# Define most common message size used for write ops
common_write_size = df[df['identifier'] == 673]['msg_size'].mode().iloc[0]

# Binary flag for anomalies in write operation size
df['write_msg_anomaly'] = ((df['identifier'] == 673) & (df['msg_size'] != common_write_size)).astype(int)

# Save to CSV
df.to_csv("//home/uwe/20250502 Network/zeek_log_ot/20250502_opcua_binary_features.csv", index=False)
print("Feature extraction complete.")
