import socket
import time
from config import *

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

# Enable port reusage so we will be able to run multiple clients and servers on single (host, port).
# server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

# Enable broadcasting mode
server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# Set a timeout so the socket does not block
# indefinitely when trying to receive data.
# todo: understand what is that!!!!
server.settimeout(0.2)
message = b""
while True:
    server.sendto(message, ('<broadcast>', client_port))
    print("message sent!")
    time.sleep(1)