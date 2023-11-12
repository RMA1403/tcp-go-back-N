from abc import ABC, abstractmethod
from Connection import Connection
from Segment import Segment

class Node(ABC):

    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    @abstractmethod
    def run() -> None:
        pass

    @abstractmethod
    def handleMessage(segment: Segment) -> None:
        pass