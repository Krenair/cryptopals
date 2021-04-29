from challenge1 import hexdecode
from challenge3 import english_freqs, single_byte_xor

if __name__ == "__main__":
    with open('4.txt') as f:
        contents = f.read()

    scores = []
    for idx, line in enumerate(contents.splitlines()):
        decoded = list(hexdecode(line))
        for keyAttempt in range(256): # brute force
            score = 0
            for ch in single_byte_xor(decoded, keyAttempt):
                lch = ch.lower() # TODO: cheating?
                score += english_freqs.get(lch, 0)
            scores.append((idx, line, keyAttempt, score))

    scores.sort(key=lambda x: x[3], reverse=True)
    idx, line, k, _ = scores[0]
    o = single_byte_xor(hexdecode(line), k)
    print('Line:', idx + 1)
    print('Key:', k)
    print('Output:', o)