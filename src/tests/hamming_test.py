from ..classes.Segment import Segment
from ..classes.SegmentFlag import SegmentFlag

with open("src/classes/data_long.txt", "r") as readfile:
    filecontent = readfile.read()
    
    # convert to byte
    data = bytes(filecontent, 'utf-8')
    
    # chunk byte file
    payloads = [data[i:i + 10] for i in range(0, len(data), 10)]
    
    flag = SegmentFlag(True, False, True)
    segment = Segment(flag, 1, 1, 0b0, data)
        
    segment.update_checksum()

    byte_segment = segment.to_bytes()
    broken = byte_segment[:1245] + b"1"

    new_segment: Segment = Segment.from_bytes(broken)
    while new_segment.detect_error():
        new_segment = Segment.from_bytes(new_segment.correct_error())
    print(new_segment.payload)