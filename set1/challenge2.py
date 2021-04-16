from challenge1 import hexdecode
def fixed_xor(s0, s1):
    print('input:', s0, s1)
    assert len(s0) == len(s1)
    d = list(hexdecode(s0)), list(hexdecode(s1))
    o = ''
    for i in range(len(d[0])):
        ob = d[0][i] ^ d[1][i] # TODO: is using python's built-in XOR cheating?
        o += f'{ob:x}' # TODO: is using python's string formatting cheating?
    print('output:', o)
    return o

if __name__ == '__main__':
    match = (fixed_xor('1c0111001f010100061a024b53535009181c', '686974207468652062756c6c277320657965') == '746865206b696420646f6e277420706c6179')
    print('correct:', match)
    assert match