from Node import Node
from Connection import Connection
from Segment import Segment
from SegmentFlag import SegmentFlag
from Parser import Parser

class Client(Node):

    def __init__(self):
        args = Parser(True)
        self.ip = "127.0.0.1"
        self.client_port, self.broadcast_port, self.pathfile_output = args.get_values()
        super().__init__(self.ip, self.client_port)
        self.client_seq_num = 1  # Set an initial sequence number

    def run(self) -> None:
        self.three_way_handshake()

    def handleMessage(segment: Segment) -> None:
        print("Handling message:", segment.payload)
    
    def three_way_handshake(self):
        self.log("Initiating three-way handshake...")
        
        # Step 1: Send SYN
        syn_segment = Segment(SegmentFlag(syn=True, ack=False, fin=False), self.client_seq_num, 0, 0, b"")
        self.connection.log_handshake(self.ip)
        self.connection.send(self.ip, self.broadcast_port, syn_segment)

        # Step 2: Receive SYN-ACK
        syn_ack_data, _ = self.connection.listen(5)
        self.syn_ack_segment = Segment.from_bytes(syn_ack_data)
        self.syn_ack_segment.log("Received SYN-ACK")

        # Step 3: Send ACK
        self.client_seq_num += 1
        ack_segment = Segment(SegmentFlag(syn=False, ack=True, fin=False), self.client_seq_num, self.syn_ack_segment.seq_num + 1, 0, b"")
        self.connection.send(self.ip, self.broadcast_port, ack_segment)
        ack_segment.log("Sent ACK")
        
        self.log("Three-way handshake finished")
    
    def down(self):
        self.log("Connection closed")
        self.connection.close()
    
    def send(self, data: bytes) -> None:
        self.log("Initiating data transfer...")
        data_segment = Segment(SegmentFlag(syn=False, ack=True, fin=False), self.client_seq_num, self.syn_ack_segment.seq_num + 1, 0, data)
        self.connection.send(self.ip, self.broadcast_port, data_segment)
        data_segment.log("Data segment sent")
    
    def receive(self):
        data_segment_data, _ = self.connection.listen(5)
        data_segment = Segment.from_bytes(data_segment_data)
        data_segment.log("Received data segment")
        print(f"Received data: {data_segment.payload.decode()}")
    

if __name__ == "__main__":
    # Client Code
    data = b"Hello World"
    client = Client()
    client.run()
    client.send(data)
    # client.receive()
    client.down()
    
# python .\Client.py 5000 5001 nigel