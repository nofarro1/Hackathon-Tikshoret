import socket
import struct
from config import *
import time
import sys
from threading import *

while True:
    client_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Enable port reusage so we will be able to run multiple clients and servers on single (host, port).
    client_udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Enable broadcasting mode
    client_udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    client_udp.bind(("", server_tcp_port))
    print("Client started, listening for offer requests...\n")
    while True:
        data, addr = client_udp.recvfrom(1024)
        if data[:4] == bytes([0xab, 0xcd, 0xdc, 0xba]) and data[4] == 0x2:
            break
    server_port = struct.unpack('>H', data[5:7])[0]
    print("Received offer from: {}, attempting to connect...".format(str(addr[0])))
    # conn_addr = client_udp.getsockname()
    # print(conn_addr)

    def handle_ans_func():
        global end_game
        ans = None
        while not ans:
            if end_game and time.time() > end_game:
                return
            else:
                ans = sys.stdin.readline()[0]
        client.sendall(str(ans).encode('utf-8'))

    #tcp client
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        # print("try to connct to: host {}, port {}".format(str(addr[0]), server_tcp_port))
        # print("type of conn_addr is {}{}".format(addr[0], addr[1]))
        client.connect((addr[0], server_tcp_port))
        name = b'ewewe'
        client.sendall(name)
        welcome = client.recv(1024).decode('utf-8')
        print(welcome)
        handle_ans = Thread(target=handle_ans_func)
        handle_ans.setDaemon(True)
        handle_ans.start()
        summary = client.recv(1024).decode('utf-8')
        print(summary)
        print("Server disconnected, listening for offer requests...\n")
