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

def export_enriched_opcua_log(instance_path, output_csv_path):
    main_log = instance_path / "opcua_binary.log"
    write_log = instance_path / "opcua_binary_write.log"

    df_main = extract_log_df(main_log)
    df_write = extract_log_df(write_log)[['opcua_link_id', 'node_id_string', 'req_status_code_link_id']]

    df_main = df_main[df_main['opcua_link_id'] != '-']
    df_write = df_write[df_write['opcua_link_id'] != '-']

    df_merged = pd.merge(df_main, df_write, on='opcua_link_id', how='left')

    df_merged.to_csv(output_csv_path, index=False)
    print(f"Enriched export saved: {output_csv_path}")

# For Single pcapng file
single_instance_path = Path("/home/uwe/20250509 Network/OT OPC UA")
output_csv_file = Path("/home/uwe/20250509_Network_OPCUA_enriched.csv")

export_enriched_opcua_log(single_instance_path, output_csv_file)
