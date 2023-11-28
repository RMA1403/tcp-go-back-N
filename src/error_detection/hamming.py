import struct

def create_parity(data: bytes) -> int:
    hamming_position = [2**x for x in range(16)]

    bin_data = 0
    for num in list(data):
        bin_data <<= 8
        bin_data |= num

    parity = 0
    for i in range(16):
        temp = bin_data
        count = 0
        for j in range(1, len(bin(bin_data)[2:]) + 16):
            if j in hamming_position:
                continue
            
            if j & (2**i) and temp & 0x1:
                count += 1

            temp >>= 1

        if count % 2 == 1:
            parity |= 2**i

    return parity

def correct_error(segment):
    error_position = create_parity(segment.payload) ^ segment.parity

    hamming_position = [2**x for x in range(16)]

    data = segment.payload

    actual_position = 0
    for i in range(error_position):
        if i in hamming_position:
            continue
        actual_position += 1

    new_data = b""
    for i in range(len(data)):
        if (len(data) - i - 1) == ((actual_position - 1) // 8):
            bin_data = list(data[i : i + 1])[0]
            corrected_data = bin_data ^ (2 ** ((actual_position - 1) % 8))
            new_data += struct.pack("B", corrected_data)
        else:
            new_data += data[i : i + 1]

    bin_data = 0
    for num in list(new_data):
        bin_data <<= 8
        bin_data |= num

    return new_data
