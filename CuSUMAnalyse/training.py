import pandas as pd
import numpy as np
import json

file_paths = ["../Datasets/Physical/csv/SWaT_Dataset_Normal_v0.csv",
              "../Datasets/Physical/csv/SWaT_Dataset_Normal_v1.csv"]

merged_df = pd.DataFrame()

for file_path in file_paths:
    df = pd.read_csv(file_path)
    df.drop([' Timestamp', 'Normal/Attack'], axis=1, inplace=True)
    merged_df = pd.concat([merged_df, df], ignore_index=True)

upper_limits = []

device_names = merged_df.columns.tolist()

parameters = []

for i, col in enumerate(device_names):
    mean = merged_df[col].mean()
    
    sample_std_dev = merged_df[col].std()
    
    k = 3  
    h = k * sample_std_dev
    
    
    
    mad = np.mean(np.abs(merged_df[col] - mean))
    if mad != 0:
        weight = 1.0 / mad
    else:
        weight = 1.0
    
    parameter = {
        "device": col,
        "weight": weight,
        "h": h,
        "upper_limit": mean + h,
        "lower_limit": mean - h
    }
    
    parameters.append(parameter)

parameters_json = json.dumps(parameters, indent=4)

with open("cusum_parameters.json", "w") as json_file:
    json_file.write(parameters_json)

print("Parametri CUSUM algoritma su sačuvani u 'cusum_parameters.json' fajl.")
