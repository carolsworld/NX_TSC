import pandas as pd


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

# === Run this for single log file ===
export_full_opcua_log(
    input_path="/home/uwe/20250502 Network/zeek_log_ot/opcua_binary.log",
    output_path="/home/uwe/20250502 Network/zeek_log_ot/20250502_opcua_binary.csv"
)
