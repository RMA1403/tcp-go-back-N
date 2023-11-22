from ..classes.Connection import Connection

HOST = "127.0.0.1"
PORT = 8765
DATA = b"Hello World"

conn = Connection(HOST, PORT)
conn.send("127.0.0.1", 5678, DATA)

conn.close()
