from Node import Node
from Parser import Parser
from Segment import Segment
from SegmentFlag import SegmentFlag

class Server(Node):

    def __init__(self):
        args = Parser(False)
        self.ip = "127.0.0.1"
        self.broadcast_port, self.pathfile_input = args.get_values()
        super().__init__(self.ip, self.broadcast_port)

    def run(self) -> None:
        self.three_way_handshake()

    def handleMessage(segment: Segment) -> None:
        print("Handling message:", segment.payload)

    def three_way_handshake(self):
        self.log("Waiting for three-way handshake...")
        
        # Step 1: Receive SYN
        syn_data, client_addr = self.connection.listen(5)
        syn_segment = Segment.from_bytes(syn_data)

        # Step 2: Send SYN-ACK
        server_seq_num = 1  # Set an initial sequence number
        syn_ack_segment = Segment(SegmentFlag(syn=True, ack=True, fin=False), server_seq_num, syn_segment.seq_num + 1, 0, b"")
        self.connection.send(client_addr[0], client_addr[1], syn_ack_segment)
        syn_ack_segment.log("Sent SYN-ACK")
        
        # Step 3: Receive ACK
        ack_data, _ = self.connection.listen(5)
        ack_segment = Segment.from_bytes(ack_data)
        ack_segment.log("Received ACK")
        
        self.log("Three-way handshake finished")
    
    def down(self):
        self.log("Connection closed")
        self.connection.close()
    
    def send(self, data: bytes) -> None:
        data_segment = Segment.data(1, 1, data)
        self.connection.send(self.client_ip, self.broadcast_port, data_segment)
        data_segment.log("Sent data segment")
    
    def receive(self):
        data_segment_data, _ = self.connection.listen(5)
        data_segment = Segment.from_bytes(data_segment_data)
        data_segment.log("Received data segment")
        print(f"Received data: {data_segment.payload.decode()}")
    
if __name__ == "__main__":
    # Server Code
    server = Server()
    server.run()
    server.receive()
    server.down()

# python Server.py 5001 data.txt