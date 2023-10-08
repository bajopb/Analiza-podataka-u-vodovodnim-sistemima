
import socket
import json
import time


csv_file_path = 'DDoSAnalyse/new_file.csv'


field_names = ["num", "date", "time", "orig", "type", "i/f_name", "i/f_dir", "src", "dst", "proto",
                "appi_name", "proxy_src_ip", "Modbus_Function_Code", "Modbus_Function_Description",
                "Modbus_Transaction_ID", "SCADA_Tag", "Modbus_Value", "service", "s_port", "Tag"]

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 51937))  
server_socket.listen(1)

print("Server je spreman za povezivanje...")

connection, address = server_socket.accept()
print(f"Povezan sa {address}")

with open(csv_file_path, 'r') as file:
    next(file)  
    for line in file:
        data = line.strip().split(',')

        data_dict = {field_names[i]: value for i, value in enumerate(data)}

        data_json = json.dumps(data_dict)
        data_str = data_json + '\n'
        print(f"Šaljem podatke komponenti za analizu: {data_str}")
        connection.send(data_str.encode())
        time.sleep(0.001)  

print("Svi podaci su poslati komponenti za analizu.")
connection.close()
server_socket.close()
