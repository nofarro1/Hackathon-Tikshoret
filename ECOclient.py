#!/usr/bin/env python3
import sys

from config import *
import socket
import time
from threading import *


HOST = 'localhost'  # The server's hostname or IP address
PORT = 1237         # The port used by the server

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

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect((HOST, server_tcp_port))
    client.sendall(b'ofar-nofir')
    welcome = client.recv(1024).decode('utf-8')
    print(welcome)
    handle_ans = Thread(target=handle_ans_func)
    handle_ans.setDaemon(True)
    handle_ans.start()
    summary = client.recv(1024).decode('utf-8')
    print(summary)
