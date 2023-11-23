import socket

from Segment import Segment


class Connection:
    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.port = port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((ip, port))

    def log(self, message: str):
        print(f"[!] {message}")
    
    def log_handshake(self, name):
        print(f"[!] [Handshake] Handshake to {name}...")
    
    def send(self, remote_ip: str, remote_port: str, data: Segment):
        self.sock.sendto(data.to_bytes(), (remote_ip, remote_port))

    def listen(self, timeout):
        self.sock.settimeout(timeout)
        return self.sock.recvfrom(32768)

    def close(self):
        self.sock.close()
    
    # def register_handler(self, handler: Callable(message: MessageInfo)
    def register_handler(self, handler: callable):
        pass
    
    def notify(self):
        pass