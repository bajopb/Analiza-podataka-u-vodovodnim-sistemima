# import pandas as pd
# import matplotlib.pyplot as plt
# from session import Session  # Pretpostavka: session.py sadrži definiciju klase Session

# # Putanja do CSV datoteke
# putanja_datoteke = "../Datasets/Network/2015-12-23_161010_76.log.part10_sorted.csv"

# # Funkcija za čitanje podataka iz CSV datoteke
# def read_data(file_path):
#     return pd.read_csv(file_path)

# # Funkcija za grupisanje podataka u sesije
# def group_data_to_sessions(df):
#     sessions = {}  # Dictionary za čuvanje trajanja sesija

#     for _, row in df.iterrows():
#         session_id = f"{row['dst']}__{row['src']}_{row['s_port']}_{row['time']}"
        
#         if session_id not in sessions:
#             # Pravimo novu sesiju i postavljamo početno i krajnje vreme
#             sessions[session_id] = Session(session_id, row['src'], row['dst'], row['s_port'])
#             sessions[session_id].start_session(row['time'])
#             sessions[session_id].end_session(row['time'])
#             # Računamo i postavljamo trajanje sesije
#             sessions[session_id].calculate_duration()
#         else:
#             # Samo osvežavamo krajnje vreme
#             sessions[session_id].end_session(row['time'])
#             # Ažuriramo trajanje sesije
#             sessions[session_id].calculate_duration()
    
#     return sessions


# # Funkcija za vizualizaciju podataka
# def visualize_data(sessions):
#     # Pretvaramo vremena trajanja sesija u brojeve (sekunde)
#     durations_seconds = [session.calculate_duration() for session in sessions.values()]

#     # Kreiramo histogram
#     plt.hist(durations_seconds, bins=20, edgecolor='black')
#     plt.title('Vreme trajanja sesija')
#     plt.xlabel('Vreme trajanja (s)')
#     plt.ylabel('Broj sesija')

#     # Prikazujemo grafiku
#     plt.show()

# # Učitaj podatke
# df = read_data(putanja_datoteke)

# # Grupišemo podatke po sesijama
# sessions = group_data_to_sessions(df)

# # Vizualizujemo podatke
# visualize_data(sessions)






# import pandas as pd
# import numpy as np

# # Učitavanje podataka iz CSV fajla
# data = pd.read_csv('../Datasets/Network/2015-12-23_161010_76.log.part10_sorted.csv')

# # Grupisanje podataka po sesijama na osnovu IP adresa i portova izvora i odredišta
# grouped_data = data.groupby(['src', 'dst', 's_port'])

# # Analiza broja sesija
# num_sessions = len(grouped_data)
# print("Ukupan broj sesija:", num_sessions)

# # Analiza trajanja sesija
# session_durations = grouped_data['time'].apply(lambda x: pd.to_datetime(x).max() - pd.to_datetime(x).min())
# avg_duration = session_durations.mean()
# min_duration = session_durations.min()
# max_duration = session_durations.max()
# print("Prosečno trajanje sesija:", avg_duration)
# print("Najkraće trajanje sesije:", min_duration)
# print("Najduže trajanje sesije:", max_duration)



# # Analiza vrsta protokola
# protocol_counts = grouped_data['proto'].nunique()
# print("Ukupan broj vrsta protokola po sesijama:")
# print(protocol_counts)

# # Analiza distribucije portova
# src_port_counts = grouped_data['s_port'].nunique()
# dst_port_counts = grouped_data['service'].nunique()
# print("Ukupan broj jedinstvenih izvornih portova po sesijama:")
# print(src_port_counts)
# print("Ukupan broj jedinstvenih odredišnih portova po sesijama:")
# print(dst_port_counts)


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





