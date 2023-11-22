from Segment import Segment

class MessageInfo:
    def __init__(self, ip: str, port: int, segment: Segment) -> None:
        self.ip = ip
        self.port = port
        self.segment = segment