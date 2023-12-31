import argparse

from .Node import Node
from ..connection.connection import Connection
from ..segment.segment import Segment
from ..segment.flag import SegmentFlag
from ..interfaces.Parseable import Parseable
from .DynamicArray import DynamicArray
from ..error_detection.hamming import correct_error 

class Client(Node, Parseable):

    def __init__(self):
        self.client_port, self.broadcast_port, self.pathfile_output = self.parse_args()
        self.ip = "127.0.0.1"
        super().__init__(self.ip, self.client_port)
        self.client_seq_num = 1  # Set an initial sequence number
        
        self.connection.connect(self.ip, self.broadcast_port)

    def parse_args(self) -> tuple[int, int, str]:
        parser = argparse.ArgumentParser(description='Client')
        parser.add_argument('client_port', metavar='[client port]', type=int, help='client port to start the service')
        parser.add_argument('broadcast_port', metavar='[broadcast port]', type=int, help='broadcast port used for destination address')
        parser.add_argument('pathfile_output', metavar='[path file output]', type=str, help='output path location')

        args = parser.parse_args()
        client_port = getattr(args, 'client_port')
        broadcast_port = getattr(args, 'broadcast_port')
        pathfile_output = getattr(args, 'pathfile_output')

        return client_port, broadcast_port, pathfile_output

    def handleMessage(segment: Segment) -> None:
        print("Handling message:", segment.payload)
    
    def down(self):
        self.log("Connection closed")
        self.connection.close()
    
    def send(self, data: Segment) -> None:
        self.log("Initiating data transfer...")
        self.connection.send(self.ip, self.broadcast_port, data)
        data.log("Data segment sent")
    
    def receive(self):
        data_segment_data, _ = self.connection.listen(5)
        if data_segment_data == None:
            return None
        data_segment = Segment.from_bytes(data_segment_data)
        data_segment.log("Received data segment")
        # print(f"Received data: {data_segment.payload.decode()}")
        return data_segment
    
    def receiveFile(self):
        dynamic_array = DynamicArray()
        eof = False
        while (not eof):
            data_segment = self.receive()
            if data_segment is not None:
                if not data_segment.is_valid_checksum():
                    data_segment.payload = correct_error(data_segment)
                    if not data_segment.is_valid_checksum():
                        continue
                
                eof = data_segment.flags.fin
                
                dynamic_array.insert(data_segment.seq_num, data_segment.payload)
                data_segment = Segment(data_segment.flags, data_segment.seq_num, data_segment.seq_num + 1, 0, 0, b"")

                if eof and dynamic_array.check_full():
                    break
                elif eof:
                    eof = False
                else:
                    self.send(data_segment)
                    
        data_segment = Segment(data_segment.flags, data_segment.seq_num, data_segment.seq_num + 1, 0, 0, b"")
        self.send(data_segment)

        byte = b""
        for i in range(dynamic_array.get_size()):
            byte += dynamic_array.get_value(i)
        
        with open(self.pathfile_output, 'wb') as file_receiver:
            file_receiver.write(byte)
            
        self.connection.initiate_close_connection(self.ip, self.broadcast_port)

if __name__ == "__main__":
    # Client Code
    data = b"Hello World"
    client = Client()
    # client.run()
    client.receiveFile()
    # client.send(data)
    # client.receive()
    # client.down()

# python -m src.classes.Server 5001 data/data_long.txt 
# python -m src.classes.Client 5000 5001 data/output/hello.txt
# python -m src.classes.Client 5002 5001 data/output/hello2.txt
