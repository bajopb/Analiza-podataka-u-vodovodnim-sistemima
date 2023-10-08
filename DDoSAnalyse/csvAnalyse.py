import os
import csv
from collections import defaultdict
from datetime import datetime
directory_path = './Datasets/Network/'

csv_files = [f for f in os.listdir(directory_path) if f.endswith('.csv')]

pair_count_by_time = defaultdict(lambda: defaultdict(int))

for csv_file_path in csv_files:
    with open(os.path.join(directory_path, csv_file_path), 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            date = row['date']
            time = row['time']
            src = row['src']
            dst = row['dst']
            current_datetime = f"{date} {time}"
            
            current_time = datetime.strptime(current_datetime, '%d%b%Y %H:%M:%S').strftime('%H:%M:%S')
            
            pair_count_by_time[current_time][(src, dst)] += 1

output_seconds_csv_file = 'learnSeconds.csv'

with open(output_seconds_csv_file, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['date', 'time', 'src', 'dst', 'count'])
    for time, pair_count in pair_count_by_time.items():
        for pair, count in pair_count.items():
            src, dst = pair
            csv_writer.writerow([date, time, src, dst, count])

print(f"Results saved to {output_seconds_csv_file}.")

pair_count_avg = defaultdict(lambda: defaultdict(float))

with open(output_seconds_csv_file, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        time = row['time']
        src = row['src']
        dst = row['dst']
        count = int(row['count'])
        
        pair_count_avg[(src, dst)]['sum'] += count
        pair_count_avg[(src, dst)]['count'] += 1

output_count_csv_file = 'learnCount.csv'

with open(output_count_csv_file, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['src', 'dst', 'average_count'])
    for pair, data in pair_count_avg.items():
        src, dst = pair
        average_count = data['sum'] / data['count'] if data['count'] > 0 else 0
        csv_writer.writerow([src, dst, average_count])

print(f"Average results saved to {output_count_csv_file}.")
