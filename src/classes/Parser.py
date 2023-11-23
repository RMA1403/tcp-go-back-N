import argparse
# python3 client.py [client port] [broadcast port] [path output]
# python3 server.py [broadcast port] [path file input]

class Parser():
    def __init__(self, is_client):
        self.client_port = ""
        self.broadcast_port = None
        self.pathfile_output = ""
        self.pathfile_input = ""
        self.is_client = is_client
        if is_client:
            parser = argparse.ArgumentParser(description='Client')
            parser.add_argument('client_port', metavar='[client port]', type=int, help='client port to start the service')
            parser.add_argument('broadcast_port', metavar='[broadcast port]', type=int, help='broadcast port used for destination address')
            parser.add_argument('pathfile_output', metavar='[path file output]', type=str, help='output path location')
            args = parser.parse_args()
            self.client_port = getattr(args, 'client_port')
            self.broadcast_port = getattr(args, 'broadcast_port')
            self.pathfile_output = getattr(args, 'pathfile_output')
        else:
            parser = argparse.ArgumentParser(description='Server')
            parser.add_argument('broadcast_port', metavar='[broadcast port]', type=int, help='broadcast port used for all client')
            parser.add_argument('pathfile_input', metavar='[Path file input]', type=str, help='path to file you want to send')
            args = parser.parse_args()
            self.broadcast_port = getattr(args, 'broadcast_port')
            self.pathfile_input = getattr(args, 'pathfile_input')
    
    def get_values(self):
        if self.is_client:
            return self.client_port, self.broadcast_port, self.pathfile_output
        else:
            return self.broadcast_port, self.pathfile_input
    
    def __str__(self):
        if self.is_client:
            return f"Client: {self.client_port} {self.broadcast_port} {self.pathfile_output}"
        else:
            return f"Server: {self.broadcast_port} {self.pathfile_input}"