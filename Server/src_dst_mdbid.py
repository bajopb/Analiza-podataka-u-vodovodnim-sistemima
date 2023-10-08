import pandas as pd
from datetime import datetime
from session import Session


data = pd.read_csv('../Datasets/Network/2015-12-23_161010_76.log.part10_sorted.csv')

data['session_id'] = (data['src'].astype(str) + '_' + data['dst'].astype(str)+'_'+data['Modbus_Transaction_ID'].astype(str)).astype(str)

grouped_data = data.groupby('session_id')

sessions = {}

for session_id, group in grouped_data:
    session = Session(session_id, group['src'].iloc[0], group['dst'].iloc[0])

    start_time = group['time'].iloc[0]
    end_time = group['time'].iloc[-1]

    start_time = pd.to_datetime(start_time)
    end_time = pd.to_datetime(end_time)

    session_duration = (end_time - start_time).total_seconds()

    session.duration = session_duration

    sessions[session_id] = session

print(len(sessions))



import statistics

average_session_duration = sum([session.duration for session in sessions.values()]) / len(sessions)

session_duration_stdev = statistics.stdev([session.duration for session in sessions.values()])

threshold =  3 * session_duration_stdev

print(f'Average session duration: {average_session_duration:.2f}')
print(f'Session duration standard deviation: {session_duration_stdev:.2f}')
print(f'Threshold: {threshold:.2f}')


import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

session_durations = [session.duration for session in sessions.values()]

session_start_times = [session.start_time for session in sessions.values()]

session_colors = ['blue' if session_duration < threshold else 'red' for session_duration in session_durations]

fig, ax = plt.subplots()

for i in range(len(session_durations)):
    session_duration = session_durations[i]
    session_start_time = session_start_times[i]
    session_color = session_colors[i]

    bar = mpatches.Rectangle((session_start_time, 0), session_duration, 1, color=session_color)
    ax.add_artist(bar)

ax.set_xlabel("Start time")

ax.set_ylabel("Session duration (seconds)")

ax.set_title("Session durations")

plt.show()
