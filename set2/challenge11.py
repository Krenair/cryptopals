import os
import random
from challenge9 import pad
from challenge10 import encrypt_aes_ecb, xor

def encrypt_aes_cbc(pt, key, iv):
    block_size = 16
    ct = []
    for i in range(int(len(pt) / len(key))):
        pt_block = pt[i*len(key):i*len(key)+block_size]
        if i == 0:
            prev_ct_block = iv
        else:
            prev_ct_block = ct[i*len(key)-block_size:i*len(key)]
        ct_block = list(encrypt_aes_ecb(list(xor(pt_block, prev_ct_block)), key))
        ct += ct_block
        yield from ct_block


def encryption_oracle(input):
    key = os.urandom(16) # TODO: is urandom cheating?

    prefix_count = random.randint(5, 10) # not cryptographically secure. doesn't need to be for this exercise
    prefix = os.urandom(prefix_count)
    suffix_count = random.randint(5, 10) # ^
    suffix = os.urandom(suffix_count)

    input = prefix + input + suffix

    if random.randint(0, 1) == 1: # assuming this is equivalent to rand(2)
        print('Mode: ECB')
        return encrypt_aes_ecb(pad(input, 16), key)
    else:
        print('Mode: CBC')
        return encrypt_aes_cbc(input, key, os.urandom(16))

if __name__ == "__main__":
    ct = list(encryption_oracle(b"ABCDABCDABCDABCD"))
    print(ct)
    # TODO: Detect the block cipher mode the function is using each time. You should end up with a piece of code that, pointed at a block box that might be encrypting ECB or CBC, tells you which one is happening.

    chunks = []
    for i in range(0, len(ct), 16):
        chunks.append(tuple(ct[i+j] for j in range(16) if i+j < len(ct)))
    unique_chunks = len(set(chunks))
    repetitions = len(chunks) - unique_chunks # going to look for line with most repeating blocks of 16 bytes
    print(len(chunks), unique_chunks, repetitions)
