import socket

HOST = '127.0.0.1'
PORT = 13117

# create the socket
server =  socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#enable the broadcast mode
server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
server.bind(('', PORT))
server.settimeout(0.2)
message = "your very important message"
while True:
    server.send(message)
    print("message sent!")
    time.sleep(1)

