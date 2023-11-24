from abc import ABC, abstractmethod

class Parseable(ABC):
    @abstractmethod
    def parse_args(self) -> tuple[int, int, str]:
        pass