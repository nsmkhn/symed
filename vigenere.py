import re

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
VALID_CHARS_REGEX_STR = "^[A-z0-9 ().,\"\n\r:;!?\'&-]+$"
PATTERN = re.compile(VALID_CHARS_REGEX_STR)

""" A B C D E F G H I J K L M N O P Q R S T U V W X Y Z 
-------------------------------------------------------
A | A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
B | B C D E F G H I J K L M N O P Q R S T U V W X Y Z A
C | C D E F G H I J K L M N O P Q R S T U V W X Y Z A B
D | D E F G H I J K L M N O P Q R S T U V W X Y Z A B C
E | E F G H I J K L M N O P Q R S T U V W X Y Z A B C D
F | F G H I J K L M N O P Q R S T U V W X Y Z A B C D E
G | G H I J K L M N O P Q R S T U V W X Y Z A B C D E F
H | H I J K L M N O P Q R S T U V W X Y Z A B C D E F G
I | I J K L M N O P Q R S T U V W X Y Z A B C D E F G H
J | J K L M N O P Q R S T U V W X Y Z A B C D E F G H I
K | K L M N O P Q R S T U V W X Y Z A B C D E F G H I J
L | L M N O P Q R S T U V W X Y Z A B C D E F G H I J K
M | M N O P Q R S T U V W X Y Z A B C D E F G H I J K L
N | N O P Q R S T U V W X Y Z A B C D E F G H I J K L M
O | O P Q R S T U V W X Y Z A B C D E F G H I J K L M N
P | P Q R S T U V W X Y Z A B C D E F G H I J K L M N O
Q | Q R S T U V W X Y Z A B C D E F G H I J K L M N O P
R | R S T U V W X Y Z A B C D E F G H I J K L M N O P Q
S | S T U V W X Y Z A B C D E F G H I J K L M N O P Q R
T | T U V W X Y Z A B C D E F G H I J K L M N O P Q R S
U | U V W X Y Z A B C D E F G H I J K L M N O P Q R S T
V | V W X Y Z A B C D E F G H I J K L M N O P Q R S T U
W | W X Y Z A B C D E F G H I J K L M N O P Q R S T U V
X | X Y Z A B C D E F G H I J K L M N O P Q R S T U V W
Y | Y Z A B C D E F G H I J K L M N O P Q R S T U V W X
Z | Z A B C D E F G H I J K L M N O P Q R S T U V W X Y """

def tabula_recta(s):
    tabula_recta = []
    for i, letter in enumerate(s):
        shifted = s[i:] + s[:i]
        tabula_recta.append({letter: shifted[i] for i, letter in enumerate(s)})
    tabula_recta = {letter: tabula_recta[i] for i, letter in enumerate(s)}
    return tabula_recta

TABULA_RECTA = tabula_recta(ALPHABET)

def encrypt_tr(plaintext, keyword, tr):
    key = keyword * (len(plaintext) // len(keyword) + 1)
    ciphertext = ''
    for i, letter in enumerate(plaintext):
        ciphertext += tr[key[i]][letter]
    return ciphertext

def decrypt_tr(ciphertext, keyword, tr):
    key = keyword * (len(ciphertext) // len(keyword) + 1)
    plaintext =  ''
    for i, letter in enumerate(ciphertext):
        plaintext += list(tr[key[i]].keys())[list(tr[key[i]].values()).index(letter)]
    return plaintext

def encrypt_alg(plaintext, keyword, alphabet):
    key = keyword * (len(plaintext) // len(keyword) + 1)
    ciphertext = ''
    for i, letter in enumerate(plaintext):
        ciphertext += alphabet[((alphabet.find(letter) + alphabet.find(key[i])) % len(alphabet))]
    return ciphertext

def decrypt_alg(ciphertext, keyword, alphabet):
    key = keyword * (len(ciphertext) // len(keyword) + 1)
    plaintext = ''
    for i, letter in enumerate(ciphertext):
        plaintext += alphabet[(alphabet.find(letter) - alphabet.find(key[i]) + len(alphabet)) % len(alphabet)]
    return plaintext

def encrypt_hex(plaintext, keyword):
    key = keyword * (len(plaintext) // len(keyword) + 1)
    plaintext_hex = ''.join(hex(ord(c))[2:].zfill(2) for c in plaintext)
    key_hex = ''.join(hex(ord(c))[2:].zfill(2) for c in key)
    ciphertext = bytearray()
    for i in range(0, len(plaintext_hex), 2):
        ciphertext += bytearray.fromhex(hex(int(plaintext_hex[i:i+2], 16) ^ int(key_hex[i:i+2], 16))[2:].zfill(2))
    return ciphertext.decode('ascii')

def decrypt_hex(ciphertext, keyword):
    key = keyword * (len(ciphertext) // len(keyword) + 1)
    ciphertext_hex = ''.join(hex(ord(c))[2:].zfill(2) for c in ciphertext)
    key_hex = ''.join(hex(ord(c))[2:].zfill(2) for c in key)
    plaintext = bytearray()
    for i in range(0, len(ciphertext_hex), 2):
        plaintext += bytearray.fromhex(hex(int(ciphertext_hex[i:i+2], 16) ^ int(key_hex[i:i+2], 16))[2:].zfill(2))
    return plaintext.decode('ascii')

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

def hack(ciphertext, pattern):
    indexes_arr = _find_indexes_of_repeated_sequences(ciphertext, 3)
    spacings = _find_spacings(indexes_arr)
    top_factors = _foreach_find_factors(spacings)[:5]
    for factor in top_factors:
        key = ''
        for substr in _build_every_nth_substr(ciphertext, factor):
            key += _bruteforce_subkey(substr, pattern)
        if len(key) == factor:
            return key
    return ''

ct = ''
with open('ciphertext', 'rb') as f:
    ct = f.read().decode('ascii')

key = hack(ct, PATTERN)
print("key:", key)
with open ('plaintext', 'w') as f:
    f.write(decrypt_hex(ct, key))
