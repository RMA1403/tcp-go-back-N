from SegmentFlag import SegmentFlag
from Segment import Segment
from Connection import Connection

# Server Code
HOST = "127.0.0.1"
PORT = 5001
server_conn = Connection(HOST, PORT)

# Step 1: Receive SYN
syn_data, client_addr = server_conn.listen(5)
syn_segment = Segment.from_bytes(syn_data)
syn_segment.log("Received SYN")

# Step 2: Send SYN-ACK
server_seq_num = 1  # Set an initial sequence number
syn_ack_segment = Segment(SegmentFlag(syn=True, ack=True, fin=False), server_seq_num, syn_segment.seq_num + 1, 0, b"")
server_conn.send(client_addr[0], client_addr[1], syn_ack_segment)
syn_ack_segment.log("Sent SYN-ACK")

# Step 3: Receive ACK
ack_data, _ = server_conn.listen(5)
ack_segment = Segment.from_bytes(ack_data)
ack_segment.log("Received ACK")

# Data transfer phase
server_conn.log("Initiating file transfer...")
data_segment_data, _ = server_conn.listen(5)
data_segment = Segment.from_bytes(data_segment_data)
data_segment.log("Received data segment")
print(f"Received data: {data_segment.payload.decode()}")

# Connection closing phase
server_conn.log("Initiating connection closing...")
fin_data, _ = server_conn.listen(5)
fin_segment = Segment.from_bytes(fin_data)
fin_segment.log("Received FIN")

server_conn.close()