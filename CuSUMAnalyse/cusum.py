import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt

def cusum_anomaly_detection(data, weight, h, upper_limit, lower_limit):
    cusum_positive = np.zeros(len(data))
    cusum_negative = np.zeros(len(data))
    anomalies = []  

    for i in range(len(data)):
        value = data[i]
        cusum_positive[i] = np.maximum(0, cusum_positive[i] + weight * (value - upper_limit))
        cusum_negative[i] = np.maximum(0, cusum_negative[i] + weight * (lower_limit - value))

        if cusum_positive[i] > h or cusum_negative[i] > h:
            anomalies.append(i)

    return anomalies

with open("cusum_parameters.json", "r") as json_file:
    parameters = json.load(json_file)

df = pd.read_csv("../Datasets/Physical/csv/SWaT_Dataset_Attack_v0.csv")
df.drop([' Timestamp', 'Normal/Attack'], axis=1, inplace=True)

data = df.values

for i, param in enumerate(parameters):
    weight = param['weight']
    h = param['h']
    upper_limit = param['upper_limit']
    lower_limit = param['lower_limit']
    device_name = param['device']
    
    anomalies = cusum_anomaly_detection(data[:, i], weight, h, upper_limit, lower_limit)
    
    x = np.arange(len(data))
    plt.figure(figsize=(15, 5))
    plt.plot(x, data[:, i], label='Podaci', color='blue')
    plt.axhline(y=upper_limit, color='green', linestyle='--', label='Gornja granica CUSUM')
    plt.axhline(y=lower_limit, color='green', linestyle='--', label='Donja granica CUSUM')
    plt.scatter(anomalies, data[anomalies, i], color='red', label='Detektovane anomalije')
    plt.xlabel('Vreme')
    plt.ylabel('Vrednost')
    plt.title(f'Analiza anomalija za uređaj: {device_name}')
    plt.legend()
    plt.savefig(f'analiza_{device_name}.png')
    plt.close()

print('Analiza završena. Grafovi su sačuvani kao PNG datoteke.')
