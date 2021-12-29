import socket
from config import *
import time
import sys
from threading import *

client_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Enable port reusage so we will be able to run multiple clients and servers on single (host, port).
client_udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Enable broadcasting mode
client_udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

client_udp.bind(("", client_port))
print("Client started, listening for offer requests...")
data, addr = client_udp.recvfrom(1024)

print("Received offer from: {}, attempting to connect...".format(str(addr[0])))

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_tcp:
#     print(addr)
#     client_tcp.connect(('127.0.0.1', client_port))
#     client_tcp.sendall(b'Ofar/n')
#     data = client_tcp.recv(1024)

#!/usr/bin/env python3

# HOST = 'localhost'  # The server's hostname or IP address
# PORT = 1237         # The port used by the server

def handle_ans_func():
    global end_game
    ans = None
    while not ans:
        if end_game and time.time() > end_game:
            return
        else:
            ans = sys.stdin.readline()[0]
            print(str(ans))
    client.sendall(str(ans).encode('utf-8'))

#tcp client
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    print("try to connct to: host {}, port {}".format(HOST, server_tcp_port))
    client.connect((HOST, server_tcp_port))
    name = b'ofir'
    client.sendall(name)
    print(name)
    welcome = client.recv(1024).decode('utf-8')
    print(welcome)
    handle_ans = Thread(target=handle_ans_func)
    handle_ans.setDaemon(True)
    handle_ans.start()
    summary = client.recv(1024).decode('utf-8')
    print(summary)
