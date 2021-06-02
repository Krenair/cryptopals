#def pad(pt, block_length):
#    padding_length = block_length - (len(pt) % block_length)
#    return pt + (padding_length * b'\x04')

def strip_padding(input, block_size):
    assert len(input) % block_size == 0
    padding_bytes = input[-1]
    assert len(set(input[-padding_bytes:])) == 1
    return input[:-padding_bytes]

if __name__ == "__main__":
    assert bytes(strip_padding(b"ICE ICE BABY\x04\x04\x04\x04", 16)) == b"ICE ICE BABY"

    try:
        print(strip_padding(b"ICE ICE BABY\x05\x05\x05\x05", 16))
    except:
        pass
    else:
        assert False

    try:
        strip_padding(b"ICE ICE BABY\x01\x02\x03\x04", 16)
    except:
        pass
    else:
        assert False