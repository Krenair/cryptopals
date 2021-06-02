def pad(pt, block_length):
    padding_length = block_length - (len(pt) % block_length)
    return pt + (padding_length * chr(padding_length).encode('ascii'))

if __name__ == "__main__":
    input = b"YELLOW SUBMARINE", 20
    output = pad(*input)
    print('output', output)
    print('len', len(output))
