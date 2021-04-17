import collections # TODO: cheating?
from challenge1 import hexdecode
english_freqs = {
    # Based on https://en.wikipedia.org/wiki/Letter_frequency
    'a': 8.2,   'b': 1.5,   'c': 2.8,  'd': 4.3, 'e': 13,  'f': 2.2,  'g': 2,   'h': 6.1,
    'i': 7,     'j': 0.15,  'k': 0.77, 'l': 4,   'm': 2.4, 'n': 6.7,  'o': 7.5, 'p': 1.9,
    'q': 0.095, 'r': 6,     's': 6.3,  't': 9.1, 'u': 2.8, 'v': 0.98, 'w': 2.4, 'x': 0.15,
    'y': 2,     'z': 0.074,
    ' ': 14 # the page says the space is more common than E, so add 1 to E's
}

def single_byte_xor(text, k):
    o = ''
    for b in text:
        o += chr(b ^ k) # TODO: cheating?
    return o

if __name__ == "__main__":
    s = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
    print('Input:', s)
    decoded = list(hexdecode(s))

    scores = collections.Counter()
    for key in range(256): # brute force
        score = 0
        for ch in single_byte_xor(decoded, key):
            lch = ch.lower() # TODO: cheating?
            score += english_freqs.get(lch, 0)
        scores[key] = score

    (k, _), *_ = scores.most_common()

    print('Key:', k)
    print('Output:', single_byte_xor(decoded, k))