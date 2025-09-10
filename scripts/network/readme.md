## How the 60 Instance OT Network Data (PCAPNG) Are Processed for Model Training

During model development, 60 separate network capture files (one per simulation instance) were collected in `.pcapng` format. Each file often contained more than 60 seconds of traffic. To ensure consistency across samples, each instance was sliced to exactly **1 minute**, typically using the **last 60 seconds** of the capture. This created a uniform structure for extracting OPC UA network features and training the model.

1. **`extractZeekLogsEnhanced.sh`**  
   Converts each `.pcapng` file to **Zeek log format** using the Zeek parser with OPC UA plugins.

2. **`extractlogtoCSV_enriched.py`**  
   Converts Zeek `.log` files to structured **CSV format** for each instance. Information from opcua_binary.log are perserved, with added "node_id_string" from opcua_binary_write.log.

3. **`extract_opcua_features_enriched.py`**  
   Extracts semantic features and combine the 60 files into 1 CSV file for model development.
   
4. **`extract_1minute.py`**  
   Slice the instance to a fixed **1-minute interval**, typically selecting the last valid minute of traffic.

### OPC UA Network Data Summary (not all the features below are used)

| Feature Name            | Description |
|-------------------------|-------------|
| `is_orig`               | Binary flag for message direction: `1` = client initiated (e.g., HMI or UAExpert), `0` = server response |
| `is_final`              | Binary flag for message completeness: `1` = complete OPC UA message, `0` = incomplete |
| `identifier`            | Numeric identifier of the OPC UA message type (e.g., `673` = WriteRequest) |
| `is_WriteOps`           | Binary flag: `1` if message is a write request (`identifier == 673`), otherwise `0` |
| `msg_size`              | Size (in bytes) of the OPC UA message |
| `write_msg_anomaly`     | Flags write requests with **uncommon message sizes** (i.e., size ≠ most common value) |
| `id.orig_p`             | Source port used by the client. Can help differentiate HMI vs. PLC or automated traffic |
| `node_id_string`        | Semantic flag gives information about which node_id has write request |

=== 

## How the Multi-Stage OT Network Data (PCAPNG) Are Processed for Prediction

During multi-stage simulation, network traffic was captured continuously in a **single `.pcapng` file** over ~5 hours. Instead of pre-slicing each instance manually, we used **timestamp-based segmentation** dynamically within the Jupyter notebook. This allowed flexible zoom-in on specific attack phases — e.g., zoom in on just Step 3 (09:45–10:15) or Step 5 (13:00–13:30).


### Processing Steps

1. **Run Zeek command  on terminal**  
   Converts the full `.pcapng` file into Zeek logs with the following commands:  
   
   **zeek -C -r theOPCUANetworkTraffic.pcapng icsnpp/opcua-binary**

2. **`extractlogtoCSV_enriched_inference.py`**  
   Converts the opcua.log file into a structured CSV file. Information from opcua_binary.log are perserved, with added "node_id_string" from opcua_binary_write.log.

3. **`extract_opcua_features_enriched_inference.py`**  
   Performs feature extraction on the full network log, including identifying write requests and their message sizes and flagging anomalous message sizes or patterns. 

   Extracts semantic features including:
   
• is_orig – whether the message was client-initiated

• is_WriteOps – whether the message is a write operation

• write_msg_anomaly – whether the write message has an unexpected size

4. **`extract_1minute_inference.py`**  
   Converts Zeek timestamps from UTC to UK local time, rounding up to minutes, assign instance number per minute, splitting the files into two csv files for import to Google Colab.
