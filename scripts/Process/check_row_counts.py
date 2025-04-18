import os
import pandas as pd

folder = '.'

# Store files with issues
invalid_files = []

# Check each file
for filename in sorted(os.listdir(folder)):
    if filename.endswith('.csv'):
        filepath = os.path.join(folder, filename)
        try:
            df = pd.read_csv(filepath, header=None)
            row_count = len(df)
            if row_count != 2000:
                invalid_files.append((filename, row_count))
        except Exception as e:
            print(f"Error reading {filename}: {e}")

# Report
if not invalid_files:
    print("All files have exactly 2000 rows!")
else:
    print("Files with row count issues:")
    for fname, count in invalid_files:
        print(f" - {fname}: {count} rows")