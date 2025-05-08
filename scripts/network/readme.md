## How the 60 Instance OT Network Data (PCAPNG) Are Processed for Model Training

During model development, 60 separate network capture files (one per simulation instance) were collected in `.pcapng` format. Each file often contained more than 60 seconds of traffic. To ensure consistency across samples, each instance was sliced to exactly **1 minute**, typically using the **last 60 seconds** of the capture. This created a uniform structure for extracting OPC UA network features and training the model.

1. **`extractZeekLogsEnhanced.sh`**  
   Converts each `.pcapng` file to **Zeek log format** using the Zeek parser with OPC UA plugins.

2. **`extractlogtoCSV.py`**  
   Converts Zeek `.log` files to structured **CSV format** (e.g., `opcua.csv`) for each instance.

3. **`extract_1minute.py`**  
   Standardizes each CSV file by slicing it to a fixed **1-minute interval**, typically selecting the last valid minute of traffic.

4. **`extract_opcua_features.py`**  
   Extracts semantic features used for model development.

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


=== 

## How the Multi-Stage OT Network Data (PCAPNG) Are Processed for Prediction

During multi-stage simulation, network traffic was captured continuously in a **single `.pcapng` file** over ~5 hours. Instead of pre-slicing each instance manually, we used **timestamp-based segmentation** dynamically within the Jupyter notebook. This allowed flexible zoom-in on specific attack phases — e.g., zoom in on just Step 3 (09:45–10:15) or Step 5 (13:00–13:30).


### Processing Steps

1. **Run Zeek command  on terminal**  
   Converts the full `.pcapng` file into Zeek logs:  
   
   **zeek -C -r yourfile.pcapng**

2. **`extractlogtoCSV_single.py`**  
   Converts the opcua.log file into a structured CSV file.

3. **`timestamp_toLocalTime.py`**  
   Converts Zeek timestamps from UTC to UK local time, aligning network events with process logs and attack chain timelines.

4. **`extract_opcua_features_single.py`**  
   Performs feature extraction on the full network log, including identifying write requests and their message sizes and flagging anomalous message sizes or patterns. 

   Extracts semantic features including:
   
• is_orig – whether the message was client-initiated

• is_WriteOps – whether the message is a write operation

• write_msg_anomaly – whether the write message has an unexpected size
