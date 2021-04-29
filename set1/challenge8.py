from challenge1 import hexdecode
if __name__ == "__main__":
	with open('8.txt') as f:
		contents = f.read()
	lines = []
	for idx, line in enumerate(contents.splitlines()):
		ct = list(hexdecode(line))
		chunks = []
		for i in range(0, len(ct), 16):
			chunks.append(tuple(ct[i+j] for j in range(16) if i+j < len(ct)))
		unique_chunks = len(set(chunks))
		repetitions = len(chunks) - unique_chunks # going to look for line with most repeating blocks of 16 bytes
		lines.append((idx, line, repetitions))

	idx, line, repetitions = max(lines, key=lambda x: x[2])
	print('line number', idx+1)
	print('repetitions', repetitions)
	print('ciphertext', bytes(hexdecode(line)))