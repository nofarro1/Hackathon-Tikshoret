#!/usr/bin/env python3

import socket
from config import *
from threading import Thread
import time

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
server_udp = None

def send_offers():
    global server_udp
    offer_message = b"abcddcba213117"
    print(server_udp)
    while count_clients < 2:
        server_udp.sendto(offer_message, ('<broadcast>', client_port))
        time.sleep(1)
    print("2 clients connected")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_tcp:
    server_tcp.bind((HOST, server_tcp_port))
    server_tcp.listen()
    print("Server started, listening on Ip address 127.0.0.1")

    # open Udp Server and sends it to the udp-server-thread
    server_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    # Enable broadcasting mode
    server_udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    udp_server_thread = Thread(target=send_offers)
    udp_server_thread.start()
    conn1, addr1 = server_tcp.accept()
    player_1, addr1 = conn1.recvfrom(1024)
    print(player_1)
    conn2, addr2 = server_tcp.accept()
    player_2, addr2 = conn2.recvfrom(1024)
    print( "{}2".format(player_2))
    count_clients = 2;
# sleep 10 secondes befor starting the game
    time.sleep(10)

    # with conn:
    #     print('Connected by', addr)
    #     while True:
    #         data = conn.recv(1024)
    #         if not data:
    #             break
    #         conn.sendall(data)
    #
    # with conn2:
    #     print('Connected by', addr2)
    #     while True:
    #         data = conn2.recv(1024)
    #         print(data)
    #         if not data:
    #             break
    #         conn2.sendall(data)