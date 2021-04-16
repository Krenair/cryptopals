def _hex_digit_to_int(d):
    if d.isnumeric():
        return int(d)
    return {
        'a': 10,
        'b': 11,
        'c': 12,
        'd': 13,
        'e': 14,
        'f': 15
    }[d]

def hexdecode(s):
    for i in range(len(s) // 2):
        yield _hex_digit_to_int(s[i*2]) * 16 + _hex_digit_to_int(s[i*2+1])

def hex2base64(s):
    print('input:', s)

    binary = ''
    for b in hexdecode(s):
        group8 = f'{b:b}' # TODO: is using python's string formatting cheating?
        binary += ('0' * (8 - (len(group8) % 8))) + group8 # prefix groups with 0s to ensure we get 8 bits

    if len(binary) % 6 > 0:
        binary += '0' * (6 - (len(binary) % 6)) # suffix groups with 0s to ensure we get a multiple of 6 bits

    o = ''
    for i in range(0, len(binary) // 6):
        d = (int(binary[i*6]) << 5) + (int(binary[i*6+1]) << 4) + (int(binary[i*6+2]) << 3) + (int(binary[i*6+3]) << 2) + (int(binary[i*6+4]) << 1) + int(binary[i*6+5])
        o += 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'[d]

    print('output:', o)
    return o

if __name__ == "__main__":
    match = (hex2base64('49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d') == 'SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t')
    print('correct:', match)
    assert match