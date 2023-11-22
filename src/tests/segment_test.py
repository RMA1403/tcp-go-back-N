from ..classes.Segment import Segment
from ..classes.SegmentFlag import SegmentFlag

flag = SegmentFlag(True, False, True)
segment = Segment(flag, 10, 1, 0b0, bytes())

print(segment.to_bytes())

test = segment.to_bytes()
new_segment = Segment.from_bytes(test)

print(new_segment.seq_num)
