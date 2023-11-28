import binascii
import argparse

from .Node import Node
from ..segment.segment import Segment
from ..segment.flag import SegmentFlag
from ..interfaces.Parseable import Parseable
from .DynamicArray import DynamicArray
import threading

class Server(Node, Parseable):

    def __init__(self):
        _, self.broadcast_port, self.pathfile_input = self.parse_args()

        self.ip = "127.0.0.1"
        super().__init__(self.ip, self.broadcast_port)
        # self.connection.node = self
        finished = False
        while  (not finished):
            self.connection.set_passive_listen(True)
            prompt = input("Apakah Anda ingin menambahkan client lain? (y/n): ")
            finished = prompt != "y"
        
        self.chunkSize = 2**15 - 14
        self.windowSize = 3
        self.payloads = None
        self.setPayloads()

    def parse_args(self) -> tuple[int, int, str]:
        parser = argparse.ArgumentParser(description='Server')
        parser.add_argument('broadcast_port', metavar='[broadcast port]', type=int, help='broadcast port used for all client')
        parser.add_argument('pathfile_input', metavar='[Path file input]', type=str, help='path to file you want to send')
        # parser.add_argument('is_broadcast', metavar='[is broadcast]', type=bool, help='broadcast or not')
        
        args = parser.parse_args()
        broadcast_port = getattr(args, 'broadcast_port')
        pathfile_input = getattr(args, 'pathfile_input')
        # is_broadcast = getattr(args, 'is_broadcast')
        
        return -1, broadcast_port, pathfile_input

    def handleMessage(segment: Segment) -> None:
        print("Handling message:", segment.payload)
    
    def down(self):
        self.log("Connection closed")
        self.connection.close()
    
    def send(self, data: Segment, client_port) -> None:
        self.connection.send(self.ip, client_port, data)
        data.log("Sent data segment")
    
    def receive(self):
        data_segment_data, _ = self.connection.listen(5)
        
        if data_segment_data == None:
            return None

        data_segment = Segment.from_bytes(data_segment_data)
        data_segment.log("Received data segment")
        # print(f"Received data: {data_segment.payload.decode()}")
        return data_segment
    
    def setPayloads(self):
        with open(self.pathfile_input, "rb") as readfile:
            data = readfile.read()
            
            # chunk byte file
            self.payloads = [data[i:i + self.chunkSize] for i in range(0, len(data), self.chunkSize)]
         
    def fileSender(self, client_port):
        self.seq_bottom = 0
        self.seq_max = self.windowSize
        while self.seq_num < len(self.payloads):
            if self.seq_bottom <= self.seq_num <= self.seq_max:
                if (self.seq_num == len(self.payloads) - 1):
                    data_segment = Segment(SegmentFlag(syn=False, ack=False, fin=True), self.seq_num, 0, 0, 0, self.payloads[self.seq_num])
                else:
                    data_segment = Segment(SegmentFlag(syn=False, ack=False, fin=False), self.seq_num, 0, 0, 0, self.payloads[self.seq_num])
                self.send(data_segment, client_port)
                self.seq_num += 1

    def ackReceiver(self):
        fin = False

        while (not fin):
            received_segmet = self.receive()

            if received_segmet is not None:

                if received_segmet.ack_num == self.seq_bottom + 1:
                    self.seq_bottom += 1
                    self.seq_max += 1
                
                fin = received_segmet.flags.fin
            else:
                self.seq_num = self.seq_bottom

    def sendFile(self, i):
        self.threads = []
        self.seq_num = 0
        
        self.threads.append(threading.Thread(target=self.fileSender, args=(self.remote_hosts[i][1],)))
        self.threads.append(threading.Thread(target=self.ackReceiver, args=()))  
        
        for thread in self.threads:
            thread.start()

        for thread in self.threads:
            thread.join()
            
        
    
if __name__ == "__main__":
    # Server Code
    server = Server()
    finished = False
    i = 0
    max_i = len(server.remote_hosts)
    start = input("Mulai mengirim untuk client pertama, port: " + str(server.remote_hosts[0][1]) + " (y/n): ")
    if start == "y":
        while (not finished) :
            server.sendFile(i)
            i+=1
            if i == max_i:
                break 
            cont = input("Lanjutkan pengiriman file untuk client ke-" + str(i+1) + ", port: " + str(server.remote_hosts[i][1]) + " (y/n): ")
            finished = cont != "y"
            
    # server.receive()
    server.connection.respond_close_connection()
    server.down()

# python -m src.classes.Server 5001 src/classes/data_long.txt