from socket import socket
from typing import Callable

from classes.MessageInfo import MessageInfo

class Connection:
    def __init__(self, ip: str, port: int, socket: socket):
        self.ip = ip
        self.port = port
        self.socket = socket

        self.handler: Callable[[MessageInfo], None] = None

    def send(self, remote_ip: str, remote_port: int):
        self.socket.send()

    def listen(self):
        pass

    def close(self):
        pass

    def register_handler(self, hanlder: Callable[[MessageInfo], None]):
        self.handler = hanlder

    def notify(self):
        pass