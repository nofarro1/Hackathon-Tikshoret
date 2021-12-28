import socket
from config import *
import time

client_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Enable port reusage so we will be able to run multiple clients and servers on single (host, port).
client_udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Enable broadcasting mode
client_udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

client_udp.bind(("", client_port))
print("Client started, listening for offer requests...")
data, addr = client_udp.recvfrom(1024)

print("Received offer from: {}, attempting to connect...".format(str(addr[0])))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_tcp:
    print(addr)
    client_tcp.connect(('127.0.0.1', server_tcp_port))
    client_tcp.sendall(b'Ofar/n')
    data = client_tcp.recv(1024)
