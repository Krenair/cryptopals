import sys
sys.path.append('../set1')

from challenge6 import base64decode
from challenge7 import decrypt_aes_ecb
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def encrypt_aes_ecb(pt, key):
    encryptor = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend()).encryptor()
    return encryptor.update(bytearray(pt)) + encryptor.finalize()

def xor(s0, s1):
    for i in range(len(s0)):
        yield s0[i] ^ s1[i] # TODO: is using python's built-in XOR cheating?

def decrypt_aes_cbc(ct, key, iv):
    for i in range(int(len(ct) / len(key))):
        ct_block = ct[i*len(key):i*len(key)+block_size]
        if i == 0:
            prev_ct_block = iv
        else:
            prev_ct_block = ct[i*len(key)-block_size:i*len(key)]
        yield from list(xor(list(decrypt_aes_ecb(ct_block, key)), prev_ct_block))

if __name__ == "__main__":
    key = b"YELLOW SUBMARINE"

    pt = b"h" * 16
    ct = encrypt_aes_ecb(pt, key)
    decrypted = decrypt_aes_ecb(ct, key)
    print(pt == decrypted)

    with open('10.txt') as f:
        contents = f.read()
    ct = list(base64decode(contents.replace('\n', '').strip()))
    #print(ct)

    block_size = 16 # TODO: is this right?
    iv = b'\x00' * block_size
    #print(iv)
    print(''.join([chr(c) for c in decrypt_aes_cbc(ct, key, iv)]))