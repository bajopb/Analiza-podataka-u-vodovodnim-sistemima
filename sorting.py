import pandas as pd
import os

directory = "./Datasets/Network/"

dataframes = []

for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        filepath = os.path.join(directory, filename)
        df = pd.read_csv(filepath)
        dataframes.append(df)

merged_df = pd.concat(dataframes, ignore_index=True)

merged_df['datetime'] = pd.to_datetime(merged_df['date'] + ' ' + merged_df['time'])

merged_df.sort_values(by='datetime', inplace=True)

output_file = "./Datasets/res/res.csv"

merged_df.to_csv(output_file, index=False)

print("Fajl je uspešno sačuvan.")
