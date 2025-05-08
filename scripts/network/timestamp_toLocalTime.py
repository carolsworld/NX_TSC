import pandas as pd
import pytz

# Load the saved CSV (UTC Time)
df = pd.read_csv("/home/uwe/20250502 Network/zeek_log_ot/20250502_opcua_binary.csv")

# Convert 'ts' column from UTC to datetime and localize to BST (UK time)
df['ts'] = pd.to_datetime(df['ts'], utc=True)
df['ts_local'] = df['ts'].dt.tz_convert('Europe/London')

# Optional: drop the original UTC column or rename it
df = df.drop(columns=['ts'])
df = df.rename(columns={'ts_local': 'ts'})

# Save the updated CSV with local timestamp
df.to_csv("/home/uwe/20250502 Network/zeek_log_ot/20250502_opcua_binary_localtime.csv", index=False)
print("Timestamps adjusted to UK local time and saved.")
