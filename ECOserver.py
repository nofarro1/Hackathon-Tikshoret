#!/usr/bin/env python3
import selectors
import socket
from config import *
from threading import Thread
import time

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
server_udp = None
conn_player_1 = None
conn_player_2 = None
username_player_1 = None
username_player_2 = None
sel = selectors.DefaultSelector()

def send_offers():
    global server_udp
    offer_message = b"abcddcba213117"
    print(server_udp)
    while count_clients < 2:
        server_udp.sendto(offer_message, ('<broadcast>', client_port))
        time.sleep(1)
    print("2 clients connected")

# def handle_accept():
#     global count_clients
#     conn, addr = server_tcp.accept()
#     count_clients += 1
#     sel.register(conn, selectors.EVENT_READ, )


def handle_player_1():
    pass


def handle_player_2():
    pass


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


    conn_player_1, addr1 = server_tcp.accept()
    username_player_1, addr1 = conn_player_1.recvfrom(1024)
    conn_player_2, addr2 = server_tcp.accept()
    username_player_2, addr2 = conn_player_2.recvfrom(1024)
    player_1_handler = Thread(target=handle_player_1)
    player_2_handler = Thread(target=handle_player_2)
    count_clients = 2;
# sleep 10 seconds before starting the game
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