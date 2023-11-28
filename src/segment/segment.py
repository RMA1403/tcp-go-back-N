import struct

from .flag import SegmentFlag
from ..error_detection.checksum import create_checksum
from ..error_detection.hamming import create_parity

class Segment:
    def __init__(
        self,
        flags: SegmentFlag,
        seq_num: int,
        ack_num: int,
        checksum: int,
        parity: int,
        payload: bytes,
    ):
        self.flags = flags
        self.seq_num = seq_num
        self.ack_num = ack_num
        self.checksum = checksum
        
        self.payload = payload
        self.parity = parity

    def __str__(self):
        return f"Segment(flags={self.flags}, seq_num={self.seq_num}, ack_num={self.ack_num}, checksum={self.checksum}, payload={self.payload}), parity={self.parity}"

    def log(self, message):
        print(f"[!] [Segment {self.seq_num}] {message}")

    def log_handshake(self, client):
        print(f"[!] [Handshake] Handshake to {client}...")

    def update_checksum(self):
        self.checksum = create_checksum(self)
        
    def update_parity(self):
        self.parity = create_parity(self.payload)

    def is_valid_checksum(self):
        print(bin(self.checksum))
        print(bin(create_checksum(self)))
        return self.checksum == create_checksum(self)

    @staticmethod
    def from_bytes(bytes: bytes):
        seq_num = struct.unpack("I", bytes[0:4])[0]
        ack_num = struct.unpack("I", bytes[4:8])[0]
        flags = SegmentFlag.from_bytes(bytes[8:9])
        checksum = struct.unpack("H", bytes[10:12])[0]
        parity = struct.unpack("H", bytes[12:14])[0]
        payload = bytes[14:]

        return Segment(flags, seq_num, ack_num, checksum, parity, payload)

    def to_bytes(self) -> bytes:
        # convert to bytes
        result = b""
        result += struct.pack("II", self.seq_num, self.ack_num)
        result += self.flags.to_bytes()
        result += struct.pack("x")
        result += struct.pack("H", self.checksum)
        result += struct.pack("H", self.parity)
        result += self.payload

        return result
