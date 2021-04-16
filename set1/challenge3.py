import collections # TODO: cheating?
from challenge1 import hexdecode
s = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
decoded = list(hexdecode(s))
print(decoded)
(most_common_char, _), *_ = collections.Counter(decoded).most_common() # get most common character
print(collections.Counter(decoded).most_common())
# most common character in English is E, so assume E maps to our most_common_char
# 'E' ^ key = most_common_char
# TODO: is this right? most_common_char ^ 'E' = key
print(most_common_char)
#alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
print(ord('E')) # TODO: cheating?
key = most_common_char ^ ord('E')
print('Chosen key', key)

o = []
for c in decoded:
	o.append(c ^ key)

print(''.join(list(map(lambda x: chr(x), o))))