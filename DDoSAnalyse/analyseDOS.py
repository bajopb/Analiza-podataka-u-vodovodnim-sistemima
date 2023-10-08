import csv
from datetime import datetime
import time
from email.mime.text import MIMEText
import smtplib

smtp_server = 'smtp.gmail.com'  
smtp_port = 587  
smtp_username = 'nikolla.vujovic@gmail.com'  
smtp_password = 'slrvywtypnlduujd' 

# Funkcija za slanje e-pošte
def send_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = 'email@example.com'  
    msg['To'] = 'nikolla.vujovic@gmail.com'  

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  
        server.login(smtp_username, smtp_password)

        server.sendmail(msg['From'], msg['To'], msg.as_string())
        print("E-pošta uspešno poslata")
    except Exception as e:
        print(f"Greška pri slanju e-pošte: {str(e)}")
    finally:
        server.quit()
input_csv_file = 'new_file.csv'

learn_count_csv_file = 'learnCount.csv'

dos_threshold = 1.3

average_counts = {}
with open(learn_count_csv_file, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)  
    for row in csvreader:
        src, dst, average_count = row
        average_counts[(src, dst)] = float(average_count)

current_datetime_str = None
current_time_pairs = {}
current_time = None

with open(input_csv_file, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    
    next(csvreader)  
    for row in csvreader:
        date = row[1]
        timeCSV = row[2]
        src = row[7]
        dst = row[8]
        current_datetime = datetime.strptime(f"{date}{timeCSV}", "%d%b%Y%H:%M:%S")
        current_datetime_str_new = current_datetime.strftime("%d%b%Y %H:%M:%S")
        if current_datetime_str_new != current_datetime_str:
            for pair, count in current_time_pairs.items():
                src, dst = pair
                if pair in average_counts:
                    average_count = average_counts[pair]
                    if count > dos_threshold * average_count:
                        warning_message = f"WARN: Uočena povećana količina saobraćaja - {src}, meta - {dst}, vreme - {current_datetime_str}"
                        print(warning_message)
                        send_email("Upozorenje: Preopterećenje saobraćaja", warning_message)
                    else:
                        print(f"OK {current_datetime_str}")
            current_datetime_str = current_datetime_str_new
            current_time_pairs = {}
            current_time = current_datetime
        if (src, dst) not in current_time_pairs:
            current_time_pairs[(src, dst)] = 0
        current_time_pairs[(src, dst)] += 1

