from challenge6 import base64decode
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

if __name__ == "__main__":
	with open('7.txt') as f:
		contents = f.read()
	ct = base64decode(contents.replace('\n', '').strip())
	key = b"YELLOW SUBMARINE"

	decryptor = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend()).decryptor()
	print((decryptor.update(bytearray(ct)) + decryptor.finalize()).decode('ascii'))