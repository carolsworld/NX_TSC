import os
import pandas as pd

folder_path = '.'

header_rows = []

for filename in sorted(os.listdir(folder_path)):
    if filename.endswith('.csv') and 'Instance' in filename:
        filepath = os.path.join(folder_path, filename)
        with open(filepath, 'r') as f:
            header = f.readline().strip()
            header_rows.append({'filename': filename, 'header': header})

header_df = pd.DataFrame(header_rows)
header_df.to_csv(os.path.join(folder_path, 'headers_check.csv'), index=False)
print("✅ Header summary saved to headers_check.csv")
