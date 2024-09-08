import socket
import json
import os
from datetime import datetime

def save_data_to_json(data):
    file_path = 'storage/data.json'
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'a') as json_file:
        json.dump(data, json_file)
        json_file.write('\n')

def run_socket_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5000))
    print('Socket server running on port 5000...')

    while True:
        data, address = server_socket.recvfrom(4096)
        print(f"Received data: {data.decode('utf-8')} from {address}")
        try:
            data_dict = eval(data.decode('utf-8'))
            current_time_str = datetime.now().isoformat()
            data_dict = {current_time_str: data_dict}
            print(data_dict)
            save_data_to_json(data_dict)
        except Exception as e:
            print(f"Error processing data: {e}")

if __name__ == "__main__":
    run_socket_server()
