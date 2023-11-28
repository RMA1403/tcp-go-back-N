from abc import ABC, abstractmethod

from ..connection.connection import Connection
from ..segment.segment import Segment


class Node(ABC):
    def __init__(self, ip: str, port: int) -> None:
        self.connection = Connection(ip, port, self)
        self.seq_num = 1

    def log(self, message: str):
        print(f"[{self.__class__.__name__}] {message}")
    
    # @abstractmethod
    # def run() -> None:
    #     pass

    @abstractmethod
    def handleMessage(segment: Segment) -> None:
        pass
