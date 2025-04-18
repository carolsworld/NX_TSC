import os
import pandas as pd

# Set paths
input_folder = "C:/Users/babya/Desktop/NX_Data"
output_folder = os.path.join(input_folder, "Step 1. Standardized")
os.makedirs(output_folder, exist_ok=True)

# Standard column order
standard_columns = [
    'instance', 'timepoint', 
    'time(sec)', 'Stand_ZPosition-value', 'Stand_RPosition-value', 'MCD_Online_Count-value',
    'MCD_GetBoxDone-value', 'Gripper_UP_Limit-value', 'Gripper_Sensor-value', 'Gripper_LO_Limit-value', 
    'RotatePosition-value', 'Gripper_Z_Speed-value', 'GetBox_signal-value', 
    'Conveyor1_Sensor-value', 'Conveyor2_Sensor-value', 'Conveyor3_Sensor-value',
    'Conveyor1_Speed-value', 'Conveyor2_Speed-value', 'Conveyor3_Speed-value', 
    'label',
]

TARGET_LENGTH = 2000  # number of rows per instance

for filename in sorted(os.listdir(input_folder)):
    if filename.endswith(".csv") and "Instance" in filename:
        filepath = os.path.join(input_folder, filename)
        df = pd.read_csv(filepath)
        original_length = len(df)

        # Adjust the length
        if original_length >= TARGET_LENGTH:
            df = df.tail(TARGET_LENGTH).reset_index(drop=True)
        else:
            # Pad with rows from the beginning
            needed = TARGET_LENGTH - original_length
            pad_rows = df.head(needed)
            df = pd.concat([pad_rows, df], ignore_index=True)

        # Extract instance number
        instance_number = int(filename.split("Instance")[1].split(".")[0])

        # Add columns
        df['instance'] = instance_number
        df['timepoint'] = list(range(TARGET_LENGTH))

        # Label assignment
        if instance_number <= 10:
            label = 0
        elif instance_number <= 20:
            label = 1
        elif instance_number <= 30:
            label = 2
        elif instance_number <= 40:
            label = 3
        elif instance_number <= 50:
            label = 4
        else:
            label = 5

        df['label'] = label

        # Reorder columns
        reordered_cols = [col for col in standard_columns if col in df.columns]
        df = df[reordered_cols]

        # Save to output folder
        output_filename = f"Instance_{instance_number:02d}_standardised_fixed.csv"
        output_path = os.path.join(output_folder, output_filename)
        df.to_csv(output_path, index=False)

        print(f"Fixed and saved: {output_filename} (original: {original_length} rows)")