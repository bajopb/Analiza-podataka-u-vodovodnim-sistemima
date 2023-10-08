import json
import socket
from collections import Counter
from threading import Semaphore

def analyze_golden_rule(session):
    print("Analiza zasnovana na zlatnom pravilu:")
    print(json.dumps(session, indent=2))

def analyze_frequency(session):
    session_id = session.get("session_id", "Nepoznata sesija")
    session_id_count = Counter({session_id: 1})
    print("Analiza frekvencije za sesiju", session_id)
    print(session_id_count)

def analyze_flow(session):
    print("Analiza toka za sesiju", session.get("session_id", "Nepoznata sesija"))
    print(json.dumps(session, indent=2))

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.connect(('localhost', 51937))  

print("Povezan sa serverom...")





def receive_and_decode_data(sock):
    received_data = b"" 

    while True:
        data_chunk = sock.recv(1024)  
        if not data_chunk:
            break 

        received_data += data_chunk  

        if b"end_of_session" in received_data:
            received_data = received_data.replace(b'"end_of_session": true', b'')
            try:
                decoded_session = json.loads(received_data.decode("utf-8"))
                print("Primljena sesija od komponente za analizu:", decoded_session)
            except json.decoder.JSONDecodeError as e:
                print("Greška pri dekodiranju JSON-a:", str(e))

            received_data = b""

receive_and_decode_data(server_socket)


print("Veza zatvorena")

