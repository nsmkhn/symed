def _find_factors(n):
    factors = []
    i = 2
    while i <= n:
        if (n % i == 0):
            factors.append(i)
        i += 1
    return factors

def _find_indexes_of_repeated_sequences(text, seq_len):
    d = {}
    for i in range(len(text)-seq_len-1):
        string = text[i:i+seq_len]
        if string not in d:
            d[string] = []
        d[string].append(i)
    return [indexes for indexes in d.values() if len(indexes) > 1]

def _find_spacings(rep_seq_indexes):
    spacings = set()
    for indexes in rep_seq_indexes:
        for i in range(len(indexes)-1):
            for j in range(i+1, len(indexes)):
                spacings.add(indexes[j]-indexes[i])
    return spacings

def _foreach_find_factors(spacings):
    factors = {}
    for spacing in spacings:
        for factor in _find_factors(spacing):
            if factor not in factors:
                factors[factor] = 0
            factors[factor] += 1
    return list(dict(sorted(factors.items(), key=lambda item: item[1], reverse = True)).keys())

def _build_every_nth_substr(ciphertext, n):
    substrings = {}
    for i, letter in enumerate(ciphertext):
        idx = i % n
        if idx not in substrings:
            substrings[idx] = ''
        substrings[idx] = substrings[idx] + letter
    return list(substrings.values())

def _bruteforce_subkey(substr, pattern):
    for key in range(128):
        substr_hex = ''.join(hex(ord(c))[2:].zfill(2) for c in substr)
        plaintext = bytearray()
        for j in range(0, len(substr_hex), 2):
            plaintext += bytearray.fromhex(hex(int(substr_hex[j:j+2], 16) ^ key)[2:].zfill(2))
        if pattern.match(plaintext.decode('ascii')):
            return chr(key)
    return ''
