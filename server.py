import socket
import time
from _thread import *
import threading
from enum import Enum


HOST = ''
PORT = 13117
client_count =0
player_1 =''
player_2 =''
socket_player1 = None
socket_player2 = None
answer =''
class State (Enum):
    player1 = 1
    game_mode = 2
state =State.waiting

# create the socket
serverUDP =  socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#enable the broadcast mode
serverUDP.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
try:
    serverUDP.bind(('', PORT))
    serverUDP.settimeout(1)
except socket.error as e:
    print (str(e))


# server started listening on socket
message = "Server started, listening on IP address 172.0.0.1"
print(message)
serverTCP.listen(2)

def acceptPlayer_1(conn):
       #todo: בשביל לנעול את האובייקט שח התשובה של השחקן, לעשות מחלקה של אטומיק-דאטה ואז ברגע ששחקן נכנס לשם ננעל את האובייקט של הדאטה והשחקן השני לא יוכל לגשת לשנול את הדאטה


def acceptPlayer_1(conn):
    data = conn.recv(2048)
    player_2 = data.decode('utf-8')

def player1_gameMode(conn):
    answer = conn.recv(2048)


def printer_offers ():
    # define message in bytes to send in broadcast
    # todo(adding const PORT)
    offer_message = b"abcddcba213117"
    while state== State.waiting:
        serverUDP.sendto(offer_message, ('<broadcast>', PORT))
        print("offer_message")
        time.sleep(1)

while True:
    printer_thread = threading.Thread(printer_offers(), (1, ))
    printer_thread.start()

   # waiting for 2 players to connect
    while state==State.waiting:
        client, addr = serverTCP.accept()
        client_count += 1
        print('connected to: '+ addr[0]+':'+ str(addr[1]))
        if client_count==1:
            socket_player1= client
            start_new_thread(acceptPlayer_1(client, ))
        else:
            socket_player1 = client
            start_new_thread(acceptPlayer_2(client, ))
            state=State.game_mode
    # printing welcome message
    time.sleep(10)
    print('Welcom to Quick Maths./n'+'Player 1: '+player_1+'/n'+ 'Player 2: '+player_2+'/n==/nPlease answer the following question as fast as you can:/nHow much is 2+2?')

    while state== State.game_mode:






