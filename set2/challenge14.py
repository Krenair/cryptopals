import sys
sys.path.append('../set1')

import os
import random

from challenge6 import base64decode
from challenge9 import pad
from challenge10 import encrypt_aes_ecb

global_key = os.urandom(16) # TODO: is urandom cheating?
with open('12.txt') as f:
    unknown_string = bytes(base64decode(f.read().replace('\n', '')))

prefix_count = random.randint(5, 10) # not cryptographically secure. doesn't need to be for this exercise
unknown_prefix = os.urandom(prefix_count)

def encryption_oracle(input):
    global global_key, unknown_string, unknown_prefix
    return encrypt_aes_ecb(pad(unknown_prefix + input + unknown_string, 16), global_key)

if __name__ == "__main__":
    block_size = 16

    ct = encryption_oracle(b'') # take ciphertext of encryption oracle with empty text
    for prefix_length in range(1, block_size): # steadily increase length of prefix
        prefix = b'A'*prefix_length
        prefixed_ct = encryption_oracle(prefix)
        if ct[:block_size] == prefixed_ct[:block_size]: # first block of ciphertext remained the same, therefore we've provided enough text to break out of the first block
            prefix = prefix[:-1] # the prefix we'll want to use will be one character shorter than what we used in this iteration
            break
        ct = prefixed_ct
    else:
        assert False

    assert len(unknown_prefix + prefix) == block_size

    search_pt = b''
    for i in range(block_size):
        one_byte_short_pt = b"A" * (block_size - i - 1)
        one_byte_short_ct = encryption_oracle(prefix + one_byte_short_pt)
        for b in range(256):
            run_pt = one_byte_short_pt + ''.join(chr(c) for c in (search_pt[len(search_pt)-i:] + bytes([b]))).encode('charmap')
            search_ct = encryption_oracle(prefix + run_pt)
            if search_ct[block_size:block_size*2] == one_byte_short_ct[block_size:block_size*2]:
                search_pt = run_pt
                print('chosen', search_pt)
                break
        else:
            assert False
