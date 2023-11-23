from SegmentFlag import SegmentFlag
from Segment import Segment
from Connection import Connection

# Client Code
data = b"Hello World"
HOST = "127.0.0.1"
PORT = 5000
SERVER_PORT = 5001
client_conn = Connection(HOST, PORT)
client_seq_num = 1  # Set an initial sequence number

# Step 1: Send SYN
syn_segment = Segment(SegmentFlag(syn=True, ack=False, fin=False), client_seq_num, 0, 0, b"")
client_conn.log("Initiating three-way handshake...")
client_conn.send(HOST, SERVER_PORT, syn_segment)

# Step 2: Receive SYN-ACK
syn_ack_data, _ = client_conn.listen(5)
syn_ack_segment = Segment.from_bytes(syn_ack_data)
syn_ack_segment.log("Received SYN-ACK")

# Step 3: Send ACK
client_seq_num += 1
ack_segment = Segment(SegmentFlag(syn=False, ack=True, fin=False), client_seq_num, syn_ack_segment.seq_num + 1, 0, b"")
client_conn.send(HOST, SERVER_PORT, ack_segment)
ack_segment.log("Sent ACK")

# Data transfer phase
client_conn.log("Initiating data transfer...")
data_segment = Segment(SegmentFlag(syn=False, ack=True, fin=False), client_seq_num, syn_ack_segment.seq_num + 1, 0, data)
client_conn.send(HOST, SERVER_PORT, data_segment)
data_segment.log("Sent data segment")

# Connection closing phase
client_conn.log("Initiating connection closing...")
fin_segment = Segment(SegmentFlag(syn=False, ack=False, fin=True), client_seq_num, 0, 0, b"")
client_conn.send(HOST, SERVER_PORT, fin_segment)
fin_segment.log("Sent FIN")

client_conn.close()
