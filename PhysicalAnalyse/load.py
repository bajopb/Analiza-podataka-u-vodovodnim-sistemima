import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

df = pd.read_csv('../Datasets/Physical/SWaT_Dataset_Attack_v0.csv')

print(df.shape)
df.head()
df.info()

df_time_start = np.array('2015-12-28T10:00:00', dtype=np.datetime64)
df_time_end = np.array('2016-01-02T02:59:59', dtype=np.datetime64)

# Visulization Strat Time and End Time
time_start = np.array('2015-12-29T00:00:00', dtype=np.datetime64)
time_end = np.array('2015-12-30T00:00:00', dtype=np.datetime64)
time_len = int((time_end - time_start) / np.timedelta64(1, 's'))

anomaly_feature = ['MV304', 'MV303', 'LIT301', 'MV303', 'AIT504', 'AIT504', 'MV101', 'LIT101', 'UV401', 'AIT502', 'P501']
anomaly_time_start = [np.array('2015-12-29T11:11:25', dtype=np.datetime64), 
                      np.array('2015-12-29T11:35:40', dtype=np.datetime64),
                      np.array('2015-12-29T11:57:25', dtype=np.datetime64),
                      np.array('2015-12-29T14:38:12', dtype=np.datetime64),
                      np.array('2015-12-29T18:15:01', dtype=np.datetime64),
                      np.array('2015-12-29T18:15:43', dtype=np.datetime64),
                      np.array('2015-12-29T18:30:00', dtype=np.datetime64),
                      np.array('2015-12-29T18:30:00', dtype=np.datetime64),
                      np.array('2015-12-29T22:55:18', dtype=np.datetime64),
                      np.array('2015-12-29T22:55:18', dtype=np.datetime64),
                      np.array('2015-12-29T22:55:18', dtype=np.datetime64)
                      ]
anomaly_time_end = [np.array('2015-12-29T11:15:17', dtype=np.datetime64), 
                    np.array('2015-12-29T11:42:50', dtype=np.datetime64),
                    np.array('2015-12-29T12:02:00', dtype=np.datetime64),
                    np.array('2015-12-29T14:50:08', dtype=np.datetime64),
                    np.array('2015-12-29T18:15:01', dtype=np.datetime64),
                    np.array('2015-12-29T18:22:17', dtype=np.datetime64),
                    np.array('2015-12-29T18:42:00', dtype=np.datetime64),
                    np.array('2015-12-29T18:42:00', dtype=np.datetime64),
                    np.array('2015-12-29T23:03:00', dtype=np.datetime64),
                    np.array('2015-12-29T23:03:00', dtype=np.datetime64),
                    np.array('2015-12-29T23:03:00', dtype=np.datetime64)
                    ]
assert len(anomaly_feature) == len(anomaly_time_start) and len(anomaly_feature) == len(anomaly_time_end)

x = time_start + np.arange(0, time_len, 1)
idx_start = int((time_start - df_time_start) / np.timedelta64(1, 's'))
idx_end = int((time_end - df_time_start) / np.timedelta64(1, 's'))

with plt.style.context('bmh'):
    font = {'color': 'darkred', 'size': 12, 'family': 'serif'}
    font_legend = {'size': 12, 'family': 'serif'}

    fig, axs = plt.subplots(51, 1, figsize=(60, 100))

    for i in range(51):
        fig, axs = plt.subplots(1, 1, figsize=(12, 6))  # 1 red, 1 kolona
        axs.plot(x, df.iloc[idx_start:idx_end, i+1], label=df.columns[i+1], color='#2f83e4')
        axs.set_xlabel('Time')
        axs.set_ylabel('Value')
        axs.legend(loc='upper left')
        if df.columns[i+1] in anomaly_feature:
            idx = anomaly_feature.index(df.columns[i+1])
            anomaly_idx = anomaly_time_start[idx] + np.arange(0, int((anomaly_time_end[idx] - anomaly_time_start[idx])/np.timedelta64(1, 's')), 1)
            anomaly_idx_start = int((anomaly_time_start[idx] - time_start)/np.timedelta64(1, 's'))
            anomaly_idx_end = int((anomaly_time_end[idx] - time_start)/np.timedelta64(1, 's'))
            axs.plot(anomaly_idx, df.iloc[idx_start + anomaly_idx_start:idx_start + anomaly_idx_end, i+1], label='{} Anomaly'.format(df.columns[i+1]), color='tomato', linewidth=6, alpha=0.8)
            axs.legend(loc='upper left')
        plt.savefig('../Visualisation/visual_{}.png'.format(df.columns[i+1]))