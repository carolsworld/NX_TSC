import pandas as pd
import os

# Define folder and files
folder = 'C:/Users/ly-lo/Desktop/NX_Data'
input_file = os.path.join(folder, 'NX_data.csv')

# Load the combined CSV
df = pd.read_csv(input_file)

# Sort by instance and timepoint
df = df.sort_values(by=['instance', 'timepoint']).reset_index(drop=True)

# Out-of-range abnormal flags
df['Conveyor1_Speed_AbnormalFlag'] = (~df['Conveyor1_Speed-value'].isin([0, 300])).astype(int)
df['Conveyor2_Speed_AbnormalFlag'] = (~df['Conveyor2_Speed-value'].isin([0, 50])).astype(int)
df['Conveyor3_Speed_AbnormalFlag'] = (~df['Conveyor3_Speed-value'].isin([0, 50])).astype(int)
df['RotatePosition_AbnormalFlag'] = (~df['RotatePosition-value'].isin([0, 90, 180])).astype(int)
df['Gripper_Z_Speed_AbnormalFlag'] = (~df['Gripper_Z_Speed-value'].isin([-400, 0, 400])).astype(int)

# Combine all three conveyor speed anomaly flags into one
df['Conveyor_Speed_AnyAbnormalFlag'] = df[
    ['Conveyor1_Speed_AbnormalFlag', 'Conveyor2_Speed_AbnormalFlag', 'Conveyor3_Speed_AbnormalFlag']
].any(axis=1).astype(int)

# Sequence-aware flag for Gripper_Z_Speed, -400 should be followed by 0, and prior with 0
def flag_gripper_z_seq_anomalies(group):
    speeds = group['Gripper_Z_Speed-value'].tolist()
    anomalies = [0] * len(speeds)

    for i in range(len(speeds) - 1):  # skip the last index
        curr_val = speeds[i]
        next_val = speeds[i + 1]

        if curr_val == 400 and next_val == -400:
            anomalies[i + 1] = 1  # flag the -400 that comes after 400

    group['Gripper_Z_Speed_SeqAnomalyFlag'] = anomalies
    return group

# Sequence anomaly for RotatePosition: flag 180 to 90 and 90 to 180
def flag_rotate_seq_anomalies(group):
    positions = group['RotatePosition-value'].tolist()
    anomalies = [0] * len(positions)
    for i in range(len(positions) - 1):
        if (positions[i] == 180 and positions[i + 1] == 90) or \
           (positions[i] == 90 and positions[i + 1] == 180):
            anomalies[i + 1] = 1
    group['RotatePosition_SeqAnomalyFlag'] = anomalies
    return group

df = df.groupby('instance', group_keys=False).apply(flag_gripper_z_seq_anomalies)
df = df.groupby('instance', group_keys=False).apply(flag_rotate_seq_anomalies).reset_index(drop=True)


# Combined Gripper_Z_Speed anomaly flag (out-of-range OR out-of-sequence)
df['Gripper_Z_Speed_CombinedAnomalyFlag'] = df[
    ['Gripper_Z_Speed_AbnormalFlag', 'Gripper_Z_Speed_SeqAnomalyFlag']
].max(axis=1)

# Combine RotatePosition flags (out-of-range OR out-of-sequence)
df['RotatePosition_CombinedAnomalyFlag'] = df[
    ['RotatePosition_AbnormalFlag', 'RotatePosition_SeqAnomalyFlag']
].max(axis=1)

# Combined abnormal flag
df['Any_Abnormal_Flag'] = df[[
    'Conveyor_Speed_AnyAbnormalFlag',
    'RotatePosition_CombinedAnomalyFlag',
    'Gripper_Z_Speed_CombinedAnomalyFlag'
]].any(axis=1).astype(int)

# Drop less useful features
columns_to_drop = [ 'time(sec)',
    'Stand_ZPosition-value', 'Stand_RPosition-value',
    'MCD_Online_Count-value', 'Gripper_UP_Limit-value',
    'Gripper_LO_Limit-value', 'Gripper_Sensor-value', 
    'Gripper_Z_Speed-value','Conveyor1_Sensor-value', 
    'Conveyor2_Sensor-value', 'Conveyor3_Sensor-value', 
    'Conveyor1_Speed-value', 'Conveyor2_Speed-value', 
    'Conveyor3_Speed-value', 'RotatePosition-value',
    'Conveyor1_Speed_AbnormalFlag', 'Conveyor2_Speed_AbnormalFlag', 'Conveyor3_Speed_AbnormalFlag',
    'Gripper_Z_Speed_AbnormalFlag', 'Gripper_Z_Speed_SeqAnomalyFlag',
    'RotatePosition_AbnormalFlag', 'RotatePosition_SeqAnomalyFlag',
    'Any_Abnormal_Flag'
]

df.drop(columns=columns_to_drop, errors='ignore', inplace=True)

# Move 'label' column to the end
label_col = df.pop('label')
df['label'] = label_col

# Split dataset based on 'instances'
df_all60instances = df.copy()
df_5scenarios = df[df['instance'] <= 50]
df_unknown = df[df['instance'] > 50]

# Save the outputs
df_all60instances.to_csv(os.path.join(folder, 'NXdata_5ScenariosaddFeatures_60instances.csv'), index=False)
df_5scenarios.to_csv(os.path.join(folder, 'NXdata_5ScenariosaddFeatures.csv'), index=False)
df_unknown.to_csv(os.path.join(folder, 'NXdata_UnknowncasesaddFeatures.csv'), index=False)

print("Saved:")
print("- NXdata_5ScenariosaddFeatures.csv (instances 1–60)")
print("- NXdata_5ScenariosaddFeatures.csv (instances 1–50)")
print("- NXdata_UnknowncasesaddFeatures.csv (instances 51–60)")