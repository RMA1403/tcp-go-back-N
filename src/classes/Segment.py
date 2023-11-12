import struct

from SegmentFlag import SegmentFlag

class Segment:
    def __init__(self, flags: SegmentFlag, seq_num: int, ack_num: int, checksum: bytes, payload: bytes):
        self.flags = flags
        self.seq_num = seq_num
        self.ack_num = ack_num
        self.checksum = checksum
        self.payload = payload
    
    def __str__(self):
        return f"Segment(flags={self.flags}, seq_num={self.seq_num}, ack_num={self.ack_num}, checksum={self.checksum}, payload={self.payload})"
    
    @staticmethod
    def syn(seq_num: int):
        pass
    
    @staticmethod
    def ack(seq_num: int, ack_num: int):
        pass
    
    @staticmethod
    def syn_ack():
        pass
    
    @staticmethod
    def fin():
        pass
    
    @staticmethod
    def fin_ack():
        pass
    
    def calculate_checksum(self):
        # using 16 bit one's complement
        data = self.to_bytes()
        # check the length of data is even
        if len(data) % 2 != 0:
            # add padding if not even
            data += b"\x00" 
        
        checksum = 0
        # calculate the sum
        for i in range(0, len(data), 2):
            checksum += (data[i] << 8) + data[i+1]
        
        # add the carry
        while checksum >> 16:
            checksum = (checksum & 0xFFFF) + (checksum >> 16)
        
        # do one's complement
        checksum = ~checksum
        
        #  return nya gmn ??
        return checksum & 0xFFFF             
    
    def update_checksum(self):
        self.checksum = self.calculate_checksum()
    
    def is_valid_checksum(self):
        return self.checksum == self.calculate_checksum()    
        
    @staticmethod
    def from_bytes(bytes: bytes):
        seq_num = struct.unpack("I", bytes[0:4])[0]
        ack_num = struct.unpack("I", bytes[4:8])[0]
        flags = SegmentFlag.from_bytes(bytes[8:9])
        checksum = struct.unpack("H", bytes[10:12])[0]
        payload = bytes[12:]

        return Segment(flags, seq_num, ack_num, checksum, payload)
    
    def to_bytes(self) -> bytes:
        # convert to bytes
        result = b""
        result += struct.pack("II", self.seq_num, self.ack_num)
        result += self.flags.to_bytes()
        result += struct.pack("x")
        result += struct.pack("H", self.checksum)
        result += self.payload

        return result