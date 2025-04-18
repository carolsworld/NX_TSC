#!/bin/bash
shopt -s nullglob

BASE_DIR="/home/uwe/Packets"
ZEEK_SCRIPT="icsnpp/opcua-binary"
SUMMARY_CSV="$BASE_DIR/zeek_logs/zeek_summary_report.csv"

cd "$BASE_DIR" || exit

# Prepare summary CSV
mkdir -p "$BASE_DIR/zeek_logs"
echo "Scenario,Instance,OPC_UA_Packets,Non_OPC_UA_Packets,Total_Packets,OPC_UA_Percentage,ZeekLog_Count,Log_Types" > "$SUMMARY_CSV"

for SCENARIO_DIR in */; do
    [[ ! -d "$SCENARIO_DIR" ]] && continue
    SCENARIO_NAME=$(basename "$SCENARIO_DIR")
    OUTPUT_DIR="$BASE_DIR/zeek_logs/$SCENARIO_NAME"
    mkdir -p "$OUTPUT_DIR"

    for PCAP_FILE in "$BASE_DIR/$SCENARIO_DIR"/*.{pcap,pcapng}; do
        [[ ! -f "$PCAP_FILE" ]] && continue

        INSTANCE_NAME=$(basename "$PCAP_FILE" | sed 's/\.[^.]*$//')
        INSTANCE_LOG_DIR="$OUTPUT_DIR/$INSTANCE_NAME"
        mkdir -p "$INSTANCE_LOG_DIR"

        # Run Zeek
        zeek -Cr "$PCAP_FILE" "$ZEEK_SCRIPT" > /dev/null 2>&1
        mv *.log "$INSTANCE_LOG_DIR/"

        # Count packets
        TOTAL_PACKETS=$(tshark -r "$PCAP_FILE" 2>/dev/null | wc -l)
        OPC_UA_PACKETS=$(tshark -r "$PCAP_FILE" -Y "opcua" 2>/dev/null | wc -l)
        NON_OPC_UA_PACKETS=$((TOTAL_PACKETS - OPC_UA_PACKETS))

        # Handle zero-division
        if [ "$TOTAL_PACKETS" -eq 0 ]; then
            OPC_UA_PERCENTAGE=0
        else
            OPC_UA_PERCENTAGE=$((100 * OPC_UA_PACKETS / TOTAL_PACKETS))
        fi

        # Count Zeek logs
        LOG_COUNT=$(ls "$INSTANCE_LOG_DIR"/*.log 2>/dev/null | wc -l)
        LOG_TYPES=$(ls "$INSTANCE_LOG_DIR"/*.log 2>/dev/null | xargs -n 1 basename | paste -sd ";" -)

        # Append to summary
        echo "$SCENARIO_NAME,$INSTANCE_NAME,$OPC_UA_PACKETS,$NON_OPC_UA_PACKETS,$TOTAL_PACKETS,$OPC_UA_PERCENTAGE%,$LOG_COUNT,\"$LOG_TYPES\"" >> "$SUMMARY_CSV"

        echo "[✓] $SCENARIO_NAME/$INSTANCE_NAME processed."
    done
done

echo "Summary written to: $SUMMARY_CSV"