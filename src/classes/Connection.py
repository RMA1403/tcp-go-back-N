import socket

from .Segment import Segment


class Connection:
    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.port = port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((ip, port))

    def send(self, remote_ip: str, remote_port: str, data: Segment):
        self.sock.sendto(data, (remote_ip, remote_port))

    def listen(self, timeout):
        self.sock.settimeout(timeout)
        return self.sock.recvfrom(32768)

    def close(self):
        self.sock.close()
