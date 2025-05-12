import pandas as pd
from pathlib import Path

def extract_log_df(path):
    with open(path, 'r') as f:
        lines = f.readlines()

    header_line = next(line for line in lines if line.startswith("#fields"))
    headers = header_line.strip().split("\t")[1:]
    data_start_index = next(i for i, line in enumerate(lines) if line.startswith("#types")) + 1
    data_lines = [line.strip().split('\t') for line in lines[data_start_index:] if not line.startswith("#")]

    df = pd.DataFrame(data_lines, columns=headers)
    df['ts'] = pd.to_datetime(df['ts'].astype(float), unit='s', errors='coerce')
    return df

def export_enriched_opcua_log(instance_path, output_path):
    main_log = instance_path / "opcua_binary.log"
    write_log = instance_path / "opcua_binary_write.log"

    df_main = extract_log_df(main_log)
    df_write = extract_log_df(write_log)[['opcua_link_id', 'node_id_string', 'req_status_code_link_id']]

    # Optional: remove rows with missing keys to avoid join problems
    df_main = df_main[df_main['opcua_link_id'] != '-']
    df_write = df_write[df_write['opcua_link_id'] != '-']

    # Merge
    df_merged = pd.merge(df_main, df_write, on='opcua_link_id', how='left')

    df_merged.to_csv(output_path, index=False)
    print(f"[✓] Enriched export saved: {output_path}")

def batch_export_enriched_logs(base_dir, output_dir):
    base_dir = Path(base_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for scenario_folder in sorted(base_dir.iterdir()):
        if scenario_folder.is_dir():
            for instance_folder in sorted(scenario_folder.iterdir()):
                if instance_folder.is_dir():
                    main_log = instance_folder / "opcua_binary.log"
                    write_log = instance_folder / "opcua_binary_write.log"
                    if main_log.exists() and write_log.exists():
                        output_csv = f"{scenario_folder.name}_{instance_folder.name.replace(' ', '_')}_opcua_enriched.csv"
                        try:
                            export_enriched_opcua_log(instance_folder, output_dir / output_csv)
                        except Exception as e:
                            print(f"[✗] Error processing {main_log}: {e}")

# Example call
batch_export_enriched_logs(
    base_dir="/home/uwe/Packets/zeek_logs",
    output_dir="/home/uwe/Packets/opcua_csv_enriched"
)
