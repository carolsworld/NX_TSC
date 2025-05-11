# Multimodal Decision Fusion for Detection of Advanced Persistent Threats in Industrial Control Systems

---
# Overview

This repository explores whether combining network, host and process indicators enhances detection of stealthy multi-step APT behaviors (especially Living off the Land techniques) in Cyber-Physical Systems and related Industrial Control Systems. 

The first goal of this simulation setup for OT process was to:
- **Detect physical process anomalies** using LSTM-FCN classifiers on time series data.
- **Identify write behaviors to PLCs** using anomaly scores from Isolation Forest.
- Ultimately, evaluate whether **fusing both sources of detection** improves detection performance — especially for **unseen, stealthy multi-vector attacks**.

The second goal of the simulation setup for IT process was to: 
- **Detect host-level anomalies** based on Wazuh SIEM logs from a Windows 11 VM under PowerShell-based attack simulation.
- **Score host behaviours per minute** using binary rule-based features derived from MITRE ATT&CK-relevant detections.
- Correlate host anomaly scores with OT behavior to support fusion-based decision making.

Ultimately, the project leverages data fusion between **OT process data**, **OT network traffic**, and **IT host event log within the OT environment** to improve detection accuracy and generalization, aiming to detect multi-step stealthy Living off the land (LOTL) technqiues.

---

# Project Overview

The goal is to evaluate whether **multi-modal data fusion** of host, network, and process data can enhance detection of stealthy APTs targeting smart manufacturing environments. This includes:

- Process-level anomaly detection (e.g. abnormal conveyor/gripper behavior)
- OPC UA network anomaly detection (e.g. unauthorized write commands)
- Host-based behavior analysis (e.g. PowerShell, living-off-the-land tools)

---

# Core Components of Digital Twin Simulation

| Modality   | Source                    | Detection Method                     | Nature | 
|------------|---------------------------|--------------------------------------|--------|
| Process    | Siemens NX MCD            | LSTM-FCN (Time Series Classifier)    |    OT  |
| Network    | Wireshark + Zeek (OPC UA) | Isolation Forest (Unsupervised)      |    OT  |
| Host Logs  | Windows 11 (Wazuh,sysmon) | Binary Rule-based Feature Scoring    |    IT  |

---

## OT Side

Both **OT process data** and **OT network traffic** were generated from Siemens NX Mechatronics Concept Designer (MCD) and Siemens PLCSimAdvanced for OT process simulation. 

Two parallel datasets were created — one for time-series classification based on multivariate process variables, and one for anomaly detection based on OPC UA network packet features.

### OT Process for Time Series Classification (Supervised - Deep Learning)
- The goal was to develop **a supervised LSTM-FCN classifier from sktime deep learning module** for detecting physical process anomalies and recognise the anomalies into multi-class.
- The multi-class include **5 scenarios**:
  - 1 normal scenario - representating an automated process with no manual intervention (Instance 1 to 10, with Label 0)
  - 4 threat scenarios with manual intervention via OPC UA clients (e.g. web-based HMI, UA Expert) to simulate stealthy APT behaviours:
    - Single-vector attacks focusing on conveyor Speed Manipulation (Instance 11 to 20, with Label 1)
    - Single-vector attacks focusing on gripper Suction Force Release (Instance 21 to 30, with Label 2)
    - Single-vector attacks focusing on gripper Z-Axis Direction Manipulation (Instance 31 to 40, with Label 3)
    - Single-vector attacks focusing on rotation Deviation (Instance 41 to 50, with Label 4)
    - Multi-vector attacks within the same time window (Instance 51 to 60, with Label 5)
- Each scenario was executed **10 times**, producing **50 instances** total as shown above.
- During the simulation runs, data is collected at a sampling rate of 0.03s intervals using NX MCD's export function.
- The dataset with 60 instances are preprocessed to ensure it only contains 1-minute simulation (**2000 timepoints per instance**) in order to fit the model training requirement.
- The data size is `2000 timepoints × 60 instances = 120,000 rows`
- Instance 1 to 50 (single-vector attacks) are **seen** datasets used for training and testing with 70:30 split, i.e. 35 instances for training, 15 instances for testing.
- Instance 51 to 60 (multi-vector attacks) are **unseen** datasets during training and testing, they are used for evaluation.  

### OT Network Traffic for Anomaly Detection (Unsupervised - Machine Learning)
- The goal was to develop **an unsupervised anomaly detection using Isolation Forest from sckit-learn** for detecting network anomalies, especially `write` requests.
- To complement the process view, network traffic between the OPC UA Server (PLC) and Client (HMI or UA Expert) was captured during the same NX MCD simulation runs.
- Network packets captured with Wireshark, parsed using Zeek (with the [OPCUA binary protocol analyzer plugin](https://github.com/cisagov/icsnpp-opcua-binary)) was used to extract all OPC UA and connection logs.
- The dataset with 60 instances are preprocessed to ensure it only contains 1-minute simulation (regardless number of network packets).
- Only the `opcua_binary.log` files containing the metadata (e.g., write counts, message sizes, source ports) are used to curate dataset.
- Key features extracted for anomaly scoring include write operation counts, message sizes, source ports, and packet totals from OPC UA logs generated from Zeek.
- The model was trained using sckit-learn IsolationForest algorithm with various contamination parameters. The parameter value of 0.25 is used as it yeilds the best result. 
- Instance 1 to 10 are **seen** training datasets used for baseline the normal network traffic, i.e. legitimate automation (**normal** cases, with Label 0). 
- Instance 11 to 60 are **unseen** testing datasets during evaluation, i.e. potential malicious write request from OPU UA Client (**anomalous** cases, with Label 1).
- The model produces anomaly scores for all 60 instances for evaluating the fusion strategy.

## IT Side

### IT Host Logs
- Logs collected from Windows 11 with Wazuh and Sysmon, including PowerShell, command line, and event-based indicators.
- Binary rule-based scoring assigns 1 point to key anomaly features per minute (e.g., suspicious logon, high-severity rule matches).
- Anomaly scores are aggregated per minute, and enriched with explanation text.
- Visual correlation with attack windows shows effective scoring and detection during simulated PowerShell-based LOTL attacks.

## Visualisation
- Grafana dashboards is to be used for visualization of fused results across modalities

## LLM Support for Analysis
- Gemini 2.0 (LLM) is used to support natural language interpretation of fused anomaly explanations.
---

## Key Findings

- Fusion of OT process + network achieves **higher F1-score** and better generalization than either modality alone.
- Host-based anomaly scoring using Wazuh rules effectively highlights LOTL-related behavior.
- Attack windows are clearly identifiable through score peaks aligned with the simulated APT timeline.


---
