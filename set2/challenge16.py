import os
from challenge9 import pad
from challenge10 import decrypt_aes_cbc, xor
from challenge11 import encrypt_aes_cbc
from challenge15 import strip_padding

def encrypt_userdata(input, key):
    sanitised = b''.join(b.to_bytes(1, byteorder='big') for b in input if b not in [ord(';'), ord('=')])
    s = b"comment1=cooking%20MCs;userdata=" + sanitised + b";comment2=%20like%20a%20pound%20of%20bacon"
    print('to encrypt', s)
    return list(encrypt_aes_cbc(pad(s, 16), key, b'\x00' * 16))

def is_admin(ct, key):
    s = strip_padding(list(decrypt_aes_cbc(ct, key, b'\x00' * 16)), 16)
    print('decrypted:', bytes(s))
    d = {}
    for kv in bytes(s).decode('charmap').split(';'):
        if '=' in kv:
            k, v, *_ = kv.split('=')
            d[k] = v
    return 'admin' in d and d['admin'] == 'true'

if __name__ == "__main__":
    key = os.urandom(16) # TODO: is urandom cheating?
    assert not is_admin(encrypt_userdata(b'hello', key), key)
    assert not is_admin(encrypt_userdata(b';admin=true', key), key)

    hax = b";admin=true"
    pt_for_replacement = b"A"*len(hax)
    hax_xored = bytes(xor(hax, pt_for_replacement))
    ct = bytearray(encrypt_userdata(pt_for_replacement, key))
    ct[16:16+len(hax)] = bytes(xor(ct[16:16+len(hax)], hax_xored))
    assert is_admin(ct, key)
    print('was admin!')