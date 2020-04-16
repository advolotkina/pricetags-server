import socket
import os
PORT = 8080
host = "10.42.0.125"
serial_number = "test123"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, PORT))
    message = "%s %s" % (serial_number, 0)
    print(message)
    s.sendall(bytes(message, 'utf8'))
    data = s.recv(1024)
print('Received', repr(data))
