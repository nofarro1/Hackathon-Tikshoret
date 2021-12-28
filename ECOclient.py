#!/usr/bin/env python3

import socket
import time

HOST = '10.100.102.76'  # The server's hostname or IP address
PORT = 65432            # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    time.sleep(10)
    s.sendall(b'Hello, world')
    data = s.recv(1024)
    time.sleep(10)


print('Received', repr(data))