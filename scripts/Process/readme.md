## How the 60 Instance OT Process CSV Files Are Processed for Model Training

During model development, 60 separate CSV files (one per simulation instance) were collected. These files often contained more than 60 seconds of process data. To standardize the dataset for time series classification, each instance was sliced to exactly **2000 timepoints**, typically selecting the **last 2000** rows to capture stable operational behavior. This ensured that every instance had a consistent structure for training.

### Processing Steps

1. **`check_headers.py`**  
   Validates that all 60 CSV files contain the expected column headers. This ensures compatibility with downstream processing scripts.

2. **`check_missingdata.py`**  
   Scans each CSV file for missing values to maintain data integrity.

3. **`standardisation.py`**  
   - Resizes each file to **2000 timepoints**
   - Adds metadata columns: `instance`, `timepoint`, and `label`
   - Labels are assigned based on instance number (e.g., 0–5 for 6 classes)

4. **`check_row_counts.py`**  
   Confirms that each CSV file contains exactly **2000 rows** post-standardization.

5. **`combinefiles.py`**  
   Merges all 60 standardized CSVs into a single file `NX_data.csv` with consistent column order and no duplicate headers.

6. **`featuresextraction_5Features.py`**  
   Extracts and engineers five key features used for model training:

   | Feature Name                          | Description |
   |---------------------------------------|-------------|
   | `MCD_GetBoxDone-value`               | Raw signal from NX MCD representing pick/place completion |
   | `GetBox_signal-value`                | Raw signal representing trigger request to retrieve box |
   | `Conveyor_Speed_AnyAbnormalFlag`     | Binary flag for any conveyor speed value not in {0, 300} (Conveyor 1) or {0, 50} (Conveyors 2 and 3) |
   | `Gripper_Z_Speed_CombinedAnomalyFlag`| Flags: <br> • Values not in {0, 400, -400} <br> • Sequence anomaly such as `400` followed by `-400` |
   | `RotatePosition_CombinedAnomalyFlag` | Flags: <br> • Values not in {0, 90, 180} <br> • Sequence transitions like `90 ↔ 180` flips |
   

---

##  How the Multi-Stage OT Process Data CSVs Are Processed for Prediction

During real-time simulation of a multi-stage attack chain, the **NX MCD export function** was used to save process data in CSV format at a fixed sampling rate of **0.03 seconds**. 

During **Step 3** of the attack chain, actuator manipulation caused the physical process to **halt unexpectedly**. This resulted in two separate CSV exports:

- **Part 1** – `20250502 Process Data_1.csv`: Covers **09:33 to ~13:26**
- **Part 2** – `20250502 Process Data_2.csv`: Covers **~13:28 (or ~13:30) to 14:33**

These files were later **combined** into a single CSV with a new column identifying the segment (`part1` or `part2`).

### Processing Step

1. **`featuresextraction_5Features_multiStage.py`**  
   Performs the same engineered feature extraction as the training stage
