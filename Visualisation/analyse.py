import socket
import json
import matplotlib.pyplot as plt
from collections import defaultdict
import math
import smtplib
from email.mime.text import MIMEText

smtp_server = 'smtp.gmail.com'  
smtp_port = 587  
smtp_username = 'nikolla.vujovic@gmail.com'  
smtp_password = '*************' 

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

interesantna_polja = ['orig', 'src', 'dst', 'proto', 'proxy_src_ip', 's_port']

broj_redova = 3
broj_kolona = 2

count_data = {polje: defaultdict(int) for polje in interesantna_polja}

fig, axs = plt.subplots(broj_redova, broj_kolona, figsize=(12, 8))

stop_execution = False

def on_close(event):
    global stop_execution
    stop_execution = True

fig.canvas.mpl_connect('close_event', on_close)

def update_chart(data, ax, polje, unknown_color='green'):
    ax.clear()
    labels, values = zip(*data.items())
    if polje == 'src':
        colors = [unknown_color if label not in known_scada_ips else 'green' for label in labels]
    else:
        colors = 'blue'
    ax.bar(labels, values, color=colors)
    ax.set_title(f'Broj pojavljivanja {polje}')
    ax.set_xlabel(polje)
    ax.set_ylabel('Broj pojavljivanja')
    ax.tick_params(axis='x', rotation=45)
    plt.tight_layout()




server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.connect(('localhost', 51937))  

print("Povezan sa serverom...")

known_scada_ips = set()

with open('scadaIPS.csv', 'r') as scada_file:
    for line in scada_file:
        line = line.strip()
        if line:
            known_scada_ips.add(line)

try:
    data_str = ''
    while not stop_execution:
        chunk = server_socket.recv(1024).decode()
        if not chunk:
            break

        data_str += chunk
        while '\n' in data_str:
            data_line, data_str = data_str.split('\n', 1)
            data = json.loads(data_line)
            

            src_address = data.get('src')
            dst_address = data.get('dst')
            att_time = data.get('time')
            if src_address is not None:
                if src_address not in known_scada_ips:
                    warning_message = f"WARN: Nepoznata SRC adresa - {src_address}, meta - {dst_address}, vreme - {att_time}"
                    print(warning_message)
                    send_email("Upozorenje: Nepoznata SRC adresa", warning_message)
                else:
                    print("OK")

            for polje in interesantna_polja:
                relevant_data = data.get(polje)
                if relevant_data is not None:
                    count_data[polje][relevant_data] += 1

                    red = math.floor(interesantna_polja.index(polje) / broj_kolona)
                    kolona = interesantna_polja.index(polje) % broj_kolona

                    update_chart(count_data[polje], axs[red, kolona], polje, unknown_color='red')


        plt.pause(0.01)  

except KeyboardInterrupt:
    print("Zaustavljeno prema zahtevu korisnika.")
finally:
    server_socket.close()

plt.show()
