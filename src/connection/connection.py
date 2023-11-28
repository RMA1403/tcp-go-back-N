import socket

from ..segment.segment import Segment
from ..segment.flag import SegmentFlag

class Connection:
    def __init__(self, ip: str, port: int, node, passive_listen: bool = False):
        self.ip = ip
        self.port = port
        
        self.node = node
        self.passive_listen = passive_listen

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((ip, port))
        
        self.listen_handshake()

    def log(self, message: str):
        print(f"[!] {message}")
    
    def log_handshake(self, name):
        print(f"[!] [Handshake] Handshake to {name}...")
        
    def set_passive_listen(self, passive_listen: bool):
        self.passive_listen = passive_listen
        
        if passive_listen:
            self.listen_handshake()
        
    def listen_handshake(self):
        if not self.passive_listen:
            print("Please set passive listen first")
            return
        
        self.log("Waiting for three-way handshake...")
        
        # Step 1: Receive SYN
        syn_data, client_addr = self.listen(30)
        syn_segment = Segment.from_bytes(syn_data)
        
        #! Gaperlu dicek???????

        # Step 2: Send SYN-ACK
        self.node.seq_num = syn_segment.seq_num + 1
        syn_ack_segment = Segment(SegmentFlag(syn=True, ack=True, fin=False), self.node.seq_num, syn_segment.seq_num + 1, 0, 0, b"")
        self.send(client_addr[0], client_addr[1], syn_ack_segment)
        syn_ack_segment.log("Sent SYN-ACK")
        
        # Step 3: Receive ACK
        ack_data, _ = self.listen(5)
        ack_segment = Segment.from_bytes(ack_data)
        ack_segment.log("Received ACK")
        
        self.log("Three-way handshake finished")
        
    def connect(self, remote_ip: str, remote_port: str):    
        self.log("Initiating three-way handshake...")
        
        # Step 1: Send SYN
        syn_segment = Segment(SegmentFlag(syn=True, ack=False, fin=False), self.node.seq_num, 0, 0, 0, b"")
        self.log_handshake(self.ip)
        self.send(remote_ip, remote_port, syn_segment)

        # Step 2: Receive SYN-ACK
        syn_ack_data, _ = self.listen(5)
        syn_ack_segment = Segment.from_bytes(syn_ack_data)
        syn_ack_segment.log("Received SYN-ACK")

        # Step 3: Send ACK
        self.node.seq_num += 1
        ack_segment = Segment(SegmentFlag(syn=False, ack=True, fin=False), self.node.seq_num, syn_ack_segment.seq_num + 1, 0, 0, b"")
        self.send(remote_ip, remote_port, ack_segment)
        ack_segment.log("Sent ACK")
        
        self.log("Three-way handshake finished")
            
    def send(self, remote_ip: str, remote_port: str, data):
        self.sock.sendto(data.to_bytes(), (remote_ip, remote_port))

    def listen(self, timeout):
        try:
            self.sock.settimeout(timeout)
            return self.sock.recvfrom(32768)
        except TimeoutError:
            return None, None

    def close(self):
        self.sock.close()
