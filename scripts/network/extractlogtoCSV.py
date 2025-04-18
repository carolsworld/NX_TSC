import pandas as pd
from pathlib import Path

def export_full_opcua_log(input_path, output_path):
    with open(input_path, 'r') as f:
        lines = f.readlines()

    header_line = next(line for line in lines if line.startswith("#fields"))
    headers = header_line.strip().split("\t")[1:]
    data_start_index = next(i for i, line in enumerate(lines) if line.startswith("#types")) + 1
    data_lines = [line.strip().split('\t') for line in lines[data_start_index:] if not line.startswith("#")]

    df = pd.DataFrame(data_lines, columns=headers)
    df['ts'] = pd.to_datetime(df['ts'].astype(float), unit='s')
    df.to_csv(output_path, index=False)
    print(f"[✓] Exported: {output_path}")

def batch_export_opcua_logs(base_dir, output_dir):
    base_dir = Path(base_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for scenario_folder in sorted(base_dir.iterdir()):
        if scenario_folder.is_dir():
            for instance_folder in sorted(scenario_folder.iterdir()):
                if instance_folder.is_dir():
                    log_path = instance_folder / "opcua_binary.log"
                    if log_path.exists():
                        output_csv_name = f"{scenario_folder.name}_{instance_folder.name.replace(' ', '_')}_opcua_full.csv"
                        output_path = output_dir / output_csv_name
                        try:
                            export_full_opcua_log(log_path, output_path)
                        except Exception as e:
                            print(f"[✗] Error in {log_path}: {e}")

# Run the batch export
batch_export_opcua_logs(
    base_dir="/home/uwe/Packets/zeek_logs",
    output_dir="/home/uwe/Packets/opcua_csv"
)