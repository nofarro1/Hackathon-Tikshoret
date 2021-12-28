import selectors
import socket
import time

from config import *

username_player_1 = None
username_player_2 = None
ans_recieved = None
addr_sender = None
conn1 = None
conn2 = None

sel = selectors.DefaultSelector()


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

    data = conn.recv(1024)
    if data:
        if not username_player_1:
            username_player_1 = data
            conn1 = conn
            print("player_1 is: {}\n".format(username_player_1))
        else:
            conn2 = conn
            sel.unregister(conn1)
            sel.unregister(conn2)
            sel.register(conn1, selectors.EVENT_WRITE, write)
            sel.register(conn2, selectors.EVENT_WRITE, write)
            username_player_2 = data
            print("player_2 is: {}2\n".format(username_player_2))
    else:
        print("the player didn't send his username!!!!")
        sel.unregister(conn)
        conn.close()


def write_summary(conn, mask):
    print("in write summary")
    msg = "Game over!\nThe correct answer was 4!\nCongragulations to the winner: {}"
    if ans_recieved == 4:
        if conn1.getpeername() == addr_sender:
            winner = username_player_1
        else:
            winner = username_player_2
    else:
        if conn1.getpeername() == addr_sender:
            winner = username_player_2
        else:
            winner = username_player_1
    conn.sendall(msg.format(winner).encode('utf-8'))

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
                sel.register(conn, selectors.EVENT_WRITE, write_summary)
                print(ans_recieved)
        except:
            return
    else:
        sel.unregister(conn)
        sel.register(conn, selectors.EVENT_WRITE, write_summary)

    if  end_game and time.time() > end_game:
        print("int end game")
        sel.unregister(conn1)
        sel.unregister(conn2)
        sel.register(conn1, selectors.EVENT_WRITE, write_summary)
        sel.register(conn2, selectors.EVENT_WRITE, write_summary)

def print_draw():
    msg = b"Game over!\nThe correct answer was 4!\nThe game ended with a draw"
    conn1.sendall(msg)
    conn2.sendall(msg)

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


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind(('localhost', 1236))
    sock.listen(2)
    sock.setblocking(False)
    sel.register(sock, selectors.EVENT_READ, accept)
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


