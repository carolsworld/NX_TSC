How the 60 instances OT network data in pcapng are converted to csv for model training?

During model development, there are 60 separate PCAP files (one per simulation instance), and their durations were often longer than 60 seconds. To standardize the dataset, we sliced each instance to exactly 1 minute, typically the last minute, assuming that was most representative of stable behavior. This gave you a uniform structure to extract features and train the model (one row per instance).

Steps
1. extractZeekLogsEnhanced.sh: from pcapng to zeek log for 60 instances
   
3. extractlogtoCSV.py: from zeek log to CSV for 60 instances
   
5. extract_1minute.py: standardise the CSV record based on 1-minute interval for 60 instances
   
7. extract opcua_features: prepare features for model development 

=== 

How the multi-stage OT network data in pcapng are converted to csv for prediction?

There is one large capture file with data covering ~5 hours. This time, we don’t need to pre-slice it using the script. Instead, we can do the 1-minute segmentation directly in the Jupyter Notebook, e.g., using groupby(pd.Grouper(freq='1min')) or defining your own custom slices for more flexible analysis. This approach provides flexibility — e.g., zoom in on just Step 3 (09:45–10:15) or Step 5 (13:00–13:30).

Steps

1. Run command "zeek .... -C -r ... " on terminal: from pcapng to zeek log for single pcapng
   
3. extractlogtoCSV_single.py: from zeek log to CSV
   
5. timestamp_toLocalTime.py: from UTC time to local time (UK)
   
3. extract_opcua_features_single.py: prepare features for data pre-processing and model prediction
