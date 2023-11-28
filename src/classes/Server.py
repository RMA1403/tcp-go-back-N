import binascii
import argparse

from .Node import Node
from ..segment.segment import Segment
from ..segment.flag import SegmentFlag
from ..interfaces.Parseable import Parseable

class Server(Node, Parseable):

    def __init__(self):
        _, self.broadcast_port, self.pathfile_input = self.parse_args()

        self.ip = "127.0.0.1"
        super().__init__(self.ip, self.broadcast_port)
        self.client_port = 5000
        
        self.connection.node = self
        self.connection.set_passive_listen(True)

    def parse_args(self) -> tuple[int, int, str]:
        parser = argparse.ArgumentParser(description='Server')
        parser.add_argument('broadcast_port', metavar='[broadcast port]', type=int, help='broadcast port used for all client')
        parser.add_argument('pathfile_input', metavar='[Path file input]', type=str, help='path to file you want to send')
        
        args = parser.parse_args()
        broadcast_port = getattr(args, 'broadcast_port')
        pathfile_input = getattr(args, 'pathfile_input')
        
        return -1, broadcast_port, pathfile_input

    def handleMessage(segment: Segment) -> None:
        print("Handling message:", segment.payload)
    
    def down(self):
        self.log("Connection closed")
        self.connection.close()
    
    def send(self, data: Segment) -> None:
        self.connection.send(self.ip, self.client_port, data)
        data.log("Sent data segment")
    
    def receive(self):
        data_segment_data, _ = self.connection.listen(5)
        
        if data_segment_data == None:
            return None

        data_segment = Segment.from_bytes(data_segment_data)
        data_segment.log("Received data segment")
        print(f"Received data: {data_segment.payload.decode()}")
        return data_segment
            
    def sendFile(self):
        # read file 
        with open(self.pathfile_input, "rb") as readfile:
            data = readfile.read()
            
            # chunk byte file
            self.chunkSize = 10
            self.windowSize = 3
            payloads = [data[i:i + self.chunkSize] for i in range(0, len(data), self.chunkSize)]
            
            seq_bottom = 0
            seq_max = self.windowSize
            seq_num = 0
            while seq_num < len(payloads):
                if seq_bottom <= seq_num <= seq_max:
                    if (seq_num == len(payloads) - 1):
                        data_segment = Segment(SegmentFlag(syn=False, ack=False, fin=True), seq_num, 0, 0, 0, payloads[seq_num])
                    else:
                        data_segment = Segment(SegmentFlag(syn=False, ack=False, fin=False), seq_num, 0, 0, 0, payloads[seq_num])
                    self.send(data_segment)
                    print(data_segment)

                    received_segmet = self.receive()
                    if received_segmet is not None:
                        seq_num += 1
                        seq_bottom += 1
                        seq_max += 1
                    else:
                        seq_num = seq_bottom
    
if __name__ == "__main__":
    # Server Code
    server = Server()
    server.sendFile()
    # server.receive()
    server.down()

# python -m src.classes.Server 5001 src/classes/hello.txt