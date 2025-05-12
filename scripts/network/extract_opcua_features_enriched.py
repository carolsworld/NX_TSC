import pandas as pd 
from pathlib import Path

# Updated folder path — replace with your enriched CSV location
source_folder = Path(r"C:\Users\ly-lo\Documents\20250509_All Steps\OT Network\1. 60 enriched csv")

# Updated columns to keep, including semantic fields
selected_columns = [
    'ts', 'uid', 'id.orig_h', 'id.orig_p', 'id.resp_h', 'id.resp_p',
    'is_orig', 'opcua_link_id', 'is_final', 'msg_size', 'identifier',
    'node_id_string'
]

# Container for all extracted data
all_instances = []

for csv_file in source_folder.glob("*.csv"):
    try:
        df = pd.read_csv(csv_file)

        # Some enriched files may not have the expected columns if merge failed
        missing_cols = [col for col in selected_columns if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Missing columns in {csv_file.name}: {missing_cols}")
        
        df = df[selected_columns]

        # Extract instance number from filename
        parts = csv_file.stem.split("_")
        instance_number = next((int(s) for s in parts if s.isdigit()), None)
        if instance_number is None:
            raise ValueError("Could not find instance number in file name")
        
        # Add instance column at front
        df.insert(0, "instance", instance_number)
        all_instances.append(df)
        print(f"Processed: {csv_file.name}")

    except Exception as e:
        print(f"Error processing {csv_file.name}: {e}")

# Combine and save
if all_instances:
    combined_df = pd.concat(all_instances, ignore_index=True)
    output_file = source_folder / "combined_opcua_dataset_instance1-60.csv"
    combined_df.to_csv(output_file, index=False)
    print(f"\nCombined dataset saved to: {output_file}")
else:
    print("No valid CSV files were processed.")