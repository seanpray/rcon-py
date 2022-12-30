import socket
import threading

__version__ = "0.1"
__doc__ = "barebones rcon implementation in python"
__author__ = "Sean Ray"
__license__ = "MIT"

HEADER_LEN = 10
MAX_PACKET = 4110

class PacketType:
    RESPONSE = 0
    CMD = 2
    AUTH = 3

class Packet:
    encoded = False
    def __init__(self, id: int, msg: str, ptype: int) -> None:
        self.len = len(msg) + HEADER_LEN
        self.id = id
        self.ptype = ptype
        self.body = msg
    def encode(self) -> bytearray:
        bytedata = []
        for v in [self.len, self.id, self.ptype]:
            bytedata.extend(v.to_bytes(2, byteorder="little"))
            bytedata.extend([0, 0])
        bytedata.extend(bytes(self.body, "ascii"))
        bytedata.extend([0, 0])
        return bytearray(bytedata)

def decode(data: bytes) -> Packet:
    plen = int.from_bytes(data[0:4], "little")
    # id is probably 4-8 but eh we don't really need it for rec
    ptype = int.from_bytes(data[8:12], "little")
    if plen < 10:
        print("invalid packet rec")
    body = str(data[12:2 + plen])
    return Packet(plen, body, ptype)


class Client:
    next = 1
    auth_state = False
    def __init__(self, host, port = 25565, timeout_ms = 15000) -> None:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(timeout_ms)
        client.connect((host, port))
        self._conn = client
        self._lock = threading.Lock()
    def auth(self, password: str):
        self.send(password, ptype = PacketType.AUTH)
        self.auth_state = True
    def next_id(self) -> int:
        current = self.next
        self.next += 1
        return current
    def send(self, data: str, ptype = PacketType.CMD) -> Packet:
        # if we aren't auth print something out, but ignore if we are trying to auth
        if not self.auth_state and ptype != PacketType.AUTH:
            print("not authenticated")
        self._lock.acquire()
        packet = Packet(self.next_id(), data, ptype)
        self._conn.send(packet.encode())
        response = decode(self._conn.recv(MAX_PACKET))
        self._lock.release()
        return response
    def close(self):
        self.auth_state = False
        self._conn.close()
