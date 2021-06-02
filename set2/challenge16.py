import os
from challenge9 import pad
from challenge10 import decrypt_aes_cbc
from challenge11 import encrypt_aes_cbc
from challenge15 import strip_padding

def encrypt_userdata(input, key):
    sanitised = b''.join(b.to_bytes(1, byteorder='big') for b in input if b not in [ord(';'), ord('=')])
    s = b"comment1=cooking%20MCs;userdata=" + sanitised + b";comment2=%20like%20a%20pound%20of%20bacon"
    return list(encrypt_aes_cbc(pad(s, 16), key, b'\x00' * 16))

def is_admin(ct, key):
    s = strip_padding(list(decrypt_aes_cbc(ct, key, b'\x00' * 16)), 16)
    d = {}
    for kv in bytes(s).decode('ascii').split(';'):
        k, v = kv.split('=')
        d[k] = v
    print(d)
    return 'admin' in d and d['admin'] == 'true'

if __name__ == "__main__":
    key = os.urandom(16) # TODO: is urandom cheating?
    assert not is_admin(encrypt_userdata(b'hello', key), key)
    assert not is_admin(encrypt_userdata(b';admin=true', key), key)

# TODO: it should not be possible to provide user input to it that will generate the string the second function is looking for.
# Instead, modify the ciphertext (without knowledge of the AES key) to accomplish this.
# You're relying on the fact that in CBC mode, a 1-bit error in a ciphertext block:
#    Completely scrambles the block the error occurs in
#    Produces the identical 1-bit error(/edit) in the next ciphertext block.