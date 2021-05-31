import sys
sys.path.append('../set1')

import os

from challenge6 import base64decode
from challenge9 import pad
from challenge10 import encrypt_aes_ecb

global_key = os.urandom(16) # TODO: is urandom cheating?
with open('12.txt') as f:
    unknown_string = bytes(base64decode(f.read().replace('\n', '')))

def encryption_oracle(input):
    global global_key
    global unknown_string
    return encrypt_aes_ecb(pad(input + unknown_string, 16), global_key)

if __name__ == "__main__":
    # step 1: Feed identical bytes of your-string to the function 1 at a time --- start with 1 byte ("A"), then "AA", then "AAA" and so on. Discover the block size of the cipher.
    block_sizes = []
    i = 1
    while len(set(block_sizes)) < 2:
        block_sizes.append(len(encryption_oracle(i * b'A')))
        i += 1

    sorted_unique_block_sizes = sorted(list(set(block_sizes)))
    block_size = sorted_unique_block_sizes[-1] - sorted_unique_block_sizes[-2]
    assert block_size == 16

    # step 2: Detect that the function is using ECB.
    pt = b"ABCD"*20
    ct = encryption_oracle(pt)
    chunks = []
    for i in range(0, len(ct), 16):
        chunks.append(tuple(ct[i+j] for j in range(16) if i+j < len(ct)))

    unique_chunks = len(set(chunks))
    repetitions = len(chunks) - unique_chunks # going to look for line with most repeating blocks of 16 bytes
    assert repetitions > 0 # ECB

    # step 3: Knowing the block size, craft an input block that is exactly 1 byte short (for instance, if the block size is 8 bytes, make "AAAAAAA"). Think about what the oracle function is going to put in that last byte position.
    one_byte_short_pt = b"A" * (block_size - 1)
    # is it going to pad?

    # step 4:  Make a dictionary of every possible last byte by feeding different strings to the oracle; for instance, "AAAAAAAA", "AAAAAAAB", "AAAAAAAC", remembering the first block of each invocation.
    pt_ct_map = {}
    for b in range(256):
        run_pt = one_byte_short_pt + chr(b).encode('charmap')
        pt_ct_map[run_pt] = encryption_oracle(run_pt)

    # step 5: Match the output of the one-byte-short input to one of the entries in your dictionary. You've now discovered the first byte of unknown-string. 
    one_byte_short_ct = encryption_oracle(one_byte_short_pt)
    for search_pt, search_ct in pt_ct_map.items():
        if search_ct[:block_size] == one_byte_short_ct[:block_size]:
            print('chosen', search_pt)
            break
    else:
        assert False

    # step 6: Repeat for the next byte.
    one_byte_short_pt = b"A" * (block_size - 2)
    pt_ct_map = {}
    for b in range(256):
        run_pt = one_byte_short_pt + ''.join(chr(c) for c in (search_pt[len(search_pt)-1:] + bytes([b]))).encode('charmap')
        pt_ct_map[run_pt] = encryption_oracle(run_pt)

    one_byte_short_ct = encryption_oracle(one_byte_short_pt)
    for search_pt, search_ct in pt_ct_map.items():
        if search_ct[:block_size] == one_byte_short_ct[:block_size]:
            print('chosen', search_pt)
            break
    else:
        assert False

    # my own step to prove we can do it for the whole first block:
    for i in range(2, block_size):
        one_byte_short_pt = b"A" * (block_size - i - 1)
        pt_ct_map = {}
        for b in range(256):
            run_pt = one_byte_short_pt + ''.join(chr(c) for c in (search_pt[len(search_pt)-i:] + bytes([b]))).encode('charmap')
            pt_ct_map[run_pt] = encryption_oracle(run_pt)

        one_byte_short_ct = encryption_oracle(one_byte_short_pt)
        for search_pt, search_ct in pt_ct_map.items():
            if search_ct[:block_size] == one_byte_short_ct[:block_size]:
                print('chosen', search_pt)
                break
        else:
            assert False
    # TODO: can we take the ciphertext and plaintext of the first block we've now found, and use it to dervive the key to get at the rest?