from ..connection.connection import Connection

HOST = "127.0.0.1"
PORT = 5678

conn = Connection(HOST, PORT)
data, addr = conn.listen(100)

print(f"Received message: {data} [from {addr}]")

conn.close()
