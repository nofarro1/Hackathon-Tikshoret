import dataclasses
import selectors
import struct

client_tcp_port = 13117
server_tcp_port = 13117


host_server = '192.168.56.1'  # Standard loopback interface address (localhost)
host_client = None
server_udp = None

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

sel = selectors.DefaultSelector()

@dataclasses.dataclass
class Message():
    Magic_cookie: bytes
    Msg_type: bytes
    Msg_server_port: bytes

    def get_port(self):
        return self.Server_port

    def get_msg_type(self):
        return self.Message_type

    def get_magic_cookie(self):
        return self.Magic_cookie

    def msg_to_bytes(self):
        return self.Magic_cookie + self.Msg_type + self.Msg_server_port


def bytes_to_msg(bytes):
    msg_type = bytes[:4]
    msg_data = bytes[4]
    port = bytes[5:7]
    return msg_type.decode("utf-8"), msg_data.deocde("utf-8"), port.decode("utf-8")

magic_cookie = bytes([0xab, 0xcd, 0xdc, 0xba])
msg_type = bytes([0x2])
msg_serv_port = struct.pack('>H', client_tcp_port)
offer_msg = Message(magic_cookie, msg_type, msg_serv_port).msg_to_bytes()

# ni.ifaddresses('eth0')[AF_LINK]   # NOTE: AF_LINK is an alias for AF_PACKET
# [{'broadcast': 'ff:ff:ff:ff:ff:ff', 'addr': '00:02:55:7b:b2:f6'}]
# ni.ifaddresses('eth0')[AF_INET]
# [{'broadcast': '172.16.161.7', 'netmask': '255.255.255.248', 'addr': '172.16.161.6'}]
#
# # eth0 ipv4 interface address
# ni.ifaddresses('eth0')[AF_INET][0]['addr']