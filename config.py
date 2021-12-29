import selectors

client_port = 13117
server_tcp_port = 13117
end_game = None
count_clients =0

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
server_udp = None
conn_player_1 = None
conn_player_2 = None
username_player_1 = None
username_player_2 = None

ans_recieved = None
addr_sender = None
conn1 = None
conn2 = None

sel = selectors.DefaultSelector()