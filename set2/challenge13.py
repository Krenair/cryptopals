import sys
sys.path.append('../set1')

import os
from challenge7 import decrypt_aes_ecb
from challenge9 import pad
from challenge10 import encrypt_aes_ecb

def parse_kv(input):
    # TODO: this is very dumb and probably vulnerable to all sorts of shenanigans. fix it up
    d = {}
    for part in input.split('&'):
        k, v = part.split('=')
        d[k] = v
    return d

def encode_kv(kv):
    return '&'.join(f'{k}={v}' for k, v in kv.items())

def profile_for(email):
    assert '&' not in email
    assert '=' not in email
    return encode_kv({'email': email, 'uid': 10, 'role': 'user'})

if __name__ == "__main__":
    input = 'foo=bar&baz=qux&zap=zazzle'
    d = parse_kv(input)
    print(d)

    profile = profile_for("foo@bar.com")
    print(profile)

    key = os.urandom(16) # TODO: is urandom cheating?
    ct = encrypt_aes_ecb(pad(profile.encode('ascii'), 16), key)
    print(ct)

    pt = decrypt_aes_ecb(ct, key)
    print(pt)

    admin_pt_block = pad(b"admin", 16)
    print(admin_pt_block)
    # need to trick the service into providing us the appropriate ciphertext for that admin block - we don't have the key
    # "email=" is 6 bytes, so to put admin in as the second block we need to set an email of 10 bytes
    admin_ct = encrypt_aes_ecb(pad(profile_for("alex@me.uk" + admin_pt_block.decode('ascii')).encode('ascii'), 16), key)
    admin_ct_block = admin_ct[16:32]

    #email=ourstring&uid=10&role=user
    # block size of 16, we want to get a single block to be user, so we can swap it out with admin
    # len("email=&uid=10&role=") = 19
    # so we want to make that 32, which means we need to set our email to be 13 bytes
    email = "alex.m@gov.uk"
    user_pt = profile_for(email)
    user_ct = encrypt_aes_ecb(pad(user_pt.encode('ascii'), 16), key)
    evil_ct = user_ct[:-16] + admin_ct_block

    evil_pt = decrypt_aes_ecb(evil_ct, key)
    print(evil_pt)