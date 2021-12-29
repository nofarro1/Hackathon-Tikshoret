#!/usr/bin/env python3
import selectors
import socket

from config import *
from threading import Thread
import time



def send_offers():
    global server_udp
    while count_clients < 2:
        server_udp.sendto(offer_msg, ('<broadcast>', server_tcp_port))
        time.sleep(1)
    server_udp.close()


def accept(sock, mask):
    global count_clients
    if count_clients < 2:
        conn, addr = sock.accept()
        count_clients += 1
        sel.register(conn, selectors.EVENT_READ, read)



def read(conn, mask):
    global username_player_1
    global username_player_2
    global conn1
    global conn2
    data = conn.recv(1024).decode('utf-8')
    if data:
        if not username_player_1:
            username_player_1 = data
            conn1 = conn
        else:
            conn2 = conn
            sel.unregister(conn1)
            sel.unregister(conn2)
            sel.register(conn1, selectors.EVENT_WRITE, write)
            sel.register(conn2, selectors.EVENT_WRITE, write)
            username_player_2 = data
    else:
        sel.unregister(conn)
        conn.close()


def write_summary():
    if ans_recieved == '4':
        if conn1.getpeername() == addr_sender:
            winner = username_player_1
        else:
            winner = username_player_2
    else:
        if conn1.getpeername() == addr_sender:
            winner = username_player_2
        else:
            winner = username_player_1
    msg = "Game over!\nThe correct answer was 4!\nCongragulations to the winner: {}".format(winner)
    conn1.sendall(msg.encode('utf-8'))
    conn2.sendall(msg.encode('utf-8'))


def read_player_answer(conn, mask):
    global ans_recieved
    global addr_sender
    global end_game

    if not ans_recieved:
        try:
            ans_recieved = conn.recv(1024).decode('utf-8')
            addr_sender = conn.getpeername()
            if ans_recieved:
                sel.unregister(conn)
                write_summary()
        except:
            return
    else:
        sel.unregister(conn)


def print_draw():
    msg = b"Game over!\nThe correct answer was 4!\nThe game ended with a draw"
    conn1.sendall(msg)
    conn2.sendall(msg)
    sel.unregister(conn1)
    sel.unregister(conn2)


def write(conn, mask):
    global username_player_1
    global username_player_2
    global end_game
    welcome_message = """Welcome to Quick Maths.
Player 1: {}
Player 2: {}
==
Please answer the following question as fast as you can:
How much is 2+2?""".format(username_player_1, username_player_2)
    conn.sendall(welcome_message.encode('utf-8'))
    if not end_game:
        end_game = time.time() + 10
    sel.unregister(conn)
    sel.register(conn, selectors.EVENT_WRITE, read_player_answer)


def tcp_server(sock):
    while not username_player_2:
        events = sel.select()
        for key, mask in events:
            callback = key.data
            callback(key.fileobj, mask)

    time.sleep(10)
    while not end_game or time.time() < end_game:
        events = sel.select()
        for key, mask in events:
            callback = key.data
            callback(key.fileobj, mask)
    if not ans_recieved:
        print_draw()


if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_tcp:
        server_tcp.bind((host_server, server_tcp_port))
        server_tcp.setblocking(False)
        server_tcp.listen(2)
        print("Server started, listening on Ip address 127.0.0.1\n")
        # print("server_tcp.getsockname() = {}".format(server_tcp.getsockname()))
        # print(server_tcp)
        sel.register(server_tcp, selectors.EVENT_READ, accept)
        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_udp:
                # restart the game #####
                ans_recieved = None
                addr_sender = None
                conn1 = None
                conn2 = None
                conn_player_1 = None
                conn_player_2 = None
                username_player_1 = None
                username_player_2 = None
                end_game = None
                count_clients = 0
                #####################

                server_udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                server_udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                server_udp.settimeout(0.2)
                udp_server_thread = Thread(target=send_offers)
                udp_server_thread.start()
                tcp_server(server_tcp)
                print("Game over, sending out offer requests...\n")