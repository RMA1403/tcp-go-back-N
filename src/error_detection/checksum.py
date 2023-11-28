def create_checksum(segment):
    # using 16 bit one's complement
    data = segment.payload
    
    # check the length of data is even
    if len(data) % 2 != 0:
        # add padding if not even
        data += b"\x00"

    # calculate the sum
    checksum = 0
    for i in range(0, len(data), 2):
        checksum += (data[i] << 8) + data[i + 1]

    # add the carry
    while checksum >> 16:
        checksum = (checksum & 0xFFFF) + (checksum >> 16)

    # do one's complement
    checksum = ~checksum

    return checksum & 0xFFFF