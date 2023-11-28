from ..segment.segment import Segment
from ..segment.flag import SegmentFlag
from ..error_detection.hamming import correct_error

with open("src/classes/data_long.txt", "r") as readfile:
    filecontent = readfile.read()
    
    # convert to byte
    data = bytes(filecontent, 'utf-8')
    
    # chunk byte file
    payloads = [data[i:i + 10] for i in range(0, len(data), 10)]
    
    flag = SegmentFlag(True, False, True)
    segment = Segment(flag, 1, 1, 0, 0, data)
        
    segment.update_checksum()
    segment.update_parity()

    byte_segment = segment.to_bytes()
    broken = byte_segment[:1247] + b"1"

    new_segment: Segment = Segment.from_bytes(broken)
    if not new_segment.is_valid_checksum():
        new_segment.payload = correct_error(new_segment)
    print(new_segment.payload)