from challenge3 import english_freqs, single_byte_xor
from challenge5 import repeating_key_xor

def base64decode(s):
    # based on https://en.wikibooks.org/wiki/Algorithm_Implementation/Miscellaneous/Base64#Javascript_2
    b64chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    padding = 0
    if s[-1] == '=':
        if s[-2] == '=':
            padding = 2
        else:
            padding = 1

    r = []
    s = s[:len(s)-padding] + ('A' * padding)
    for c in range(0, len(s), 4):
        n = (b64chars.index(s[c]) << 18) + (b64chars.index(s[c+1]) << 12) + (b64chars.index(s[c+2]) << 6) + b64chars.index(s[c+3])
        r += [
            (n >> 16) & 255,
            (n >> 8) & 255,
            n & 255
        ]

    o = r[:len(r)-padding]
    return o

def hamming(s1, s2): # step 2
    assert len(s1) == len(s2) # ensure they're the same length
    score = 0
    for c1, c2 in zip(s1, s2): # get each character
        for b1, b2 in zip('{:08b}'.format(c1), '{:08b}'.format(c2)): # get each bit
            if b1 != b2: # if the bits don't match...
                score += 1 # increase the score

    return score

if __name__ == "__main__":
    with open('6.txt') as f:
        data = f.read().replace('\n', '')

    decoded = base64decode(data)
    keysizes = []
    for keysize in range(2, 40+1): # step 1
        distances = []
        for i in range(0, len(decoded), keysize*2)[:-1]:
            distances.append(hamming(decoded[i:i+keysize], decoded[i+keysize:i+keysize*2]) / keysize)
        keysizes.append((keysize, sum(distances)/len(distances))) # step 3

    keysize, _ = min(keysizes, key=lambda x: x[1]) # step 4

    blocks = []
    for i in range(0, len(decoded), keysize):
        blocks.append([decoded[i+j] for j in range(0, keysize) if i+j < len(decoded)]) # step 5

    oblocks = []
    for i in range(keysize):
        oblocks.append([block[i] for block in blocks if i < len(block)]) # step 6

    # just some checks to ensure everything is transposed correctly
    for n in range(len(blocks)):
        for m in range(keysize):
            idx = (n * keysize) + m
            if idx < len(decoded):
                assert blocks[n][m] == oblocks[m][n]
                assert blocks[n][m] == decoded[idx]

    ks = []
    for block in oblocks:
        scores = []
        for keyAttempt in range(256): # brute force
            score = 0
            for ch in single_byte_xor(block, keyAttempt):
                lch = ch.lower() # TODO: cheating?
                score += english_freqs.get(lch, 0)
            scores.append((keyAttempt, score))

        k, _ = max(scores, key=lambda x: x[1]) # step 7
        ks.append(k) # step 8

    print('key', ks)

    o = ''.join([chr(c) for c in repeating_key_xor(decoded, ks)])
    print(o)