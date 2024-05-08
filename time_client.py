import socket
import json
import base64
import logging

server_address=('127.0.0.1', 45000)

def send_command(command_str=""):
    global server_address
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    logging.warning(f"Connecting to {server_address}")
    try:
        logging.warning(f"Sending command '{command_str}'")
        sock.sendall(command_str.encode())
        # Look for the response, waiting until socket is done (no more data)
        data_received="" #empty string
        while True:
            #socket does not receive all data at once, data comes in part, need to be concatenated at the end of process
            data = sock.recv(16)
            if data:
                #data is not empty, concat with previous content
                data_received += data.decode()
                if "\r\n" in data_received:
                    break
            else:
                # no more data, stop the process by break
                break
        # at this point, data_received (string) will contain all data coming from the socket
        # to be able to use the data_received as a dict, need to load it using json.loads()

        logging.warning("Data received from server:")
        return data_received
    except Exception as e:
        print(str(e))
        logging.warning("Error during data receiving")
        return False


if __name__=='__main__':
    print(send_command('TIME\r\nQUIT\r\n'))
    print(send_command('TIM\r\nQUIT\r\n'))
    print(send_command('TIME\r\nQUI\r\n'))