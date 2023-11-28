from abc import ABC, abstractmethod

from .Connection import Connection
from ..segment.segment import Segment


class Node(ABC):
    def __init__(self, ip: str, port: int) -> None:
        self.connection = Connection(ip, port) 

    def log(self, message: str):
        print(f"[{self.__class__.__name__}] {message}")
    
    @abstractmethod
    def run() -> None:
        pass

    @abstractmethod
    def handleMessage(segment: Segment) -> None:
        pass
