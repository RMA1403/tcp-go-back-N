import threading

class SendThread:
    def __init__(self, connection, segment, remote_ip, remote_port):
        self.connection = connection
        self.segment = segment
        self.remote_ip = remote_ip
        self.remote_port = remote_port
        
        self.thread = threading.Thread(target=self.send_segment)
        self.is_running = False

    def start(self):
        if not self.is_running():
            self.is_running = True
            self.thread.start()
            
    def stop(self):
        self.is_running = False
        self.thread.join()
        
    def send_segment(self):
        while self.is_running():
            self.connection.send(self.remote_ip, self.remote_port, self.segment)
            