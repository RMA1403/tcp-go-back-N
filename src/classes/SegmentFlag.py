import struct

SYN = 0b00010
ACK = 0b10000
FIN = 0b00001

class SegmentFlag:
    def __init__(self, syn: bool, ack: bool, fin: bool):
        self.syn = syn
        self.ack = ack
        self.fin = fin  
    
    def to_bytes(self) -> bytes:
        bytes = 0b0
        if self.syn:
            bytes &= SYN
        if self.ack:
            bytes &= ACK
        if self.fin:
            bytes &= FIN

        return struct.pack("B", bytes)

    @staticmethod
    def from_bytes(bytes: bytes):
        binary = struct.unpack("B", bytes)[0]

        syn = bool((binary >> 1) & 0b1)
        ack = bool((binary >> 4) & 0b1)
        fin = bool(binary & 0b1)

        return SegmentFlag(syn, ack, fin)