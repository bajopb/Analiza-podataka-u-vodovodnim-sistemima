import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
from cusum import CusumDetector

df = pd.read_csv('../Datasets/Physical/SWaT_Dataset_Attack_v0.csv')
df.drop(' Timestamp', axis=1, inplace=True)
df.drop('Normal/Attack', axis=1, inplace=True)
column_names = df.columns
from sklearn import preprocessing
processor = preprocessing.MinMaxScaler()
df = processor.fit_transform(df)
np.save('../data/swat-2015-data.npy', df)

data = np.load('../data/swat-2015-data.npy')

df_time_start = np.array('2015-12-28T10:00:00', dtype=np.datetime64)
df_time_end = np.array('2016-01-02T02:59:59', dtype=np.datetime64)
time_start = np.array('2015-12-29T00:00:00', dtype=np.datetime64)
time_end = np.array('2015-12-30T00:00:00', dtype=np.datetime64)

idx_start = int((time_start - df_time_start) / np.timedelta64(1, 's'))
idx_end = int((time_end - df_time_start) / np.timedelta64(1, 's'))

sample = data[idx_start:idx_end, 1]

import sys; sys.path.append('../')

threshold_cusum = 1.5
cusum_detector = CusumDetector(threshold=threshold_cusum)
anomaly_score_cusum = cusum_detector.detect(sample)

x = range(idx_end - idx_start)

with plt.style.context('bmh'):
    font = {'color': 'darkred', 'size': 12, 'family': 'serif'}
    font_legend = {'size': 12, 'family': 'serif'}

    fig, axs = plt.subplots(51, 1, figsize=(60, 100))

    for i in range(51):
        anomaly_score_i = anomaly_score_cusum[i].flatten()  # Ensure anomaly_score_list[i] has the correct dimensions
        axs[i].plot(x, anomaly_score_i, label=column_names[i+1], color='#2f83e4')
        axs[i].set_xlabel('Time', fontdict=font)
        axs[i].set_ylabel('Anomaly Score', fontdict=font)
        axs[i].legend(loc='upper right', prop=font_legend)
        labels = axs[i].get_xticklabels() + axs[i].get_yticklabels()
        [label.set_fontname('serif') for label in labels]

plt.savefig('../Visualisation/swat-2015-sr.png')

anomaly_score_list = []
for i in range(51):
    sample = data[idx_start:idx_end, i]
    anomaly_score = cusum_detector.detect(sample)
    anomaly_score_list.append(anomaly_score)

x = range(idx_end - idx_start)

with plt.style.context('bmh'):
    fig, axs = plt.subplots(51, 1, figsize=(60, 100))

    for i in range(51):
        axs[i].plot(x, anomaly_score_list[i], label=df.columns[i+1], color='#2f83e4')
        axs[i].set_xlabel('Time')
        axs[i].set_ylabel('Anomaly Score')
        axs[i].legend(loc='upper right')

plt.savefig('../Visualisation/swat-2015-cusum.png')

sample = data[idx_start:idx_end, 1]

from statsmodels.tsa.seasonal import seasonal_decompose
result = seasonal_decompose(sample, period=2000, extrapolate_trend='freq')
trend = result.trend

x = range(idx_end - idx_start)

with plt.style.context('bmh'):
    fig, axs = plt.subplots(2, 1, figsize=(20, 5))

    axs[0].plot(x, sample, label='Original Data', color='#2f83e4')
    axs[0].set_xlabel('Time')
    axs[0].set_ylabel('Value')
    axs[0].legend(loc='upper right')

    axs[1].plot(x, trend, label='Seasonality Remove', color='tomato')
    axs[1].set_xlabel('Time')
    axs[1].set_ylabel('Value')
    axs[1].legend(loc='upper right')

plt.tight_layout()
plt.savefig('../Visualisation/swat-2015-seasonal-remove.png')

threshold_cusum = 1.5
cusum_detector = CusumDetector(threshold=threshold_cusum)
anomaly_score = cusum_detector.detect(sample)

anomaly_score[83000:] = 0
anomaly_score[:2000] = 0

x = range(idx_end - idx_start)

with plt.style.context('bmh'):
    fig, axs = plt.subplots(3, 1, figsize=(20, 10))

    axs[0].plot(x, sample, label='Original Data', color='#2f83e4')
    axs[0].set_xlabel('Time')
    axs[0].set_ylabel('Value')
    axs[0].set_title('Original Data')
    axs[0].legend(loc='upper right')

    axs[1].plot(x, trend, label='Seasonality Remove', color='mediumturquoise')
    axs[1].set_xlabel('Time')
    axs[1].set_ylabel('Value')
    axs[1].set_title('Seasonality Remove')
    axs[1].legend(loc='upper right')

    axs[2].plot(x, anomaly_score, label='CUSUM Processed', color='tomato')
    axs[2].set_xlabel('Time')
    axs[2].set_ylabel('Value')
    axs[2].set_title('CUSUM Processed')
    axs[2].legend(loc='upper right')

plt.tight_layout()
plt.savefig('../Visualisation/swat-2015-seasonal-cusum.png')
