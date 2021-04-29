pt = """Burning 'em, if you ain't quick and nimble
I go crazy when I hear a cymbal"""

def str_to_bytearray(text):
    return [ord(c) for c in text] # TODO: cheating?

def repeating_key_xor(text, k):
    for i, b in enumerate(text):
        kb = k[i % len(k)]
        yield b ^ kb

if __name__ == "__main__":
    o = ''
    for c in repeating_key_xor(str_to_bytearray(pt), str_to_bytearray('ICE')):
        o += f'{c:02x}' # TODO: cheating?
    print(o)