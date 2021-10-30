import re
import helpers

ENCODING = 'ascii'
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
TABULA_RECTA = helpers._tabula_recta(ALPHABET)
VALID_CHARS_REGEX_STR = "^[A-z0-9 ().,\"\n\r:;!?\'&-]+$"
PATTERN = re.compile(VALID_CHARS_REGEX_STR)
BASE_HEX = 16
SEQUENCE_LEN_SEEK = 3
NUM_TRY_FACTORS = 5

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
        ciphertext += bytearray.fromhex(hex(int(plaintext_hex[i:i+2], BASE_HEX) ^ int(key_hex[i:i+2], BASE_HEX))[2:].zfill(2))
    return ciphertext.decode(ENCODING)

def decrypt_hex(ciphertext, keyword):
    key = keyword * (len(ciphertext) // len(keyword) + 1)
    ciphertext_hex = ''.join(hex(ord(c))[2:].zfill(2) for c in ciphertext)
    key_hex = ''.join(hex(ord(c))[2:].zfill(2) for c in key)
    plaintext = bytearray()
    for i in range(0, len(ciphertext_hex), 2):
        plaintext += bytearray.fromhex(hex(int(ciphertext_hex[i:i+2], BASE_HEX) ^ int(key_hex[i:i+2], BASE_HEX))[2:].zfill(2))
    return plaintext.decode(ENCODING)

def hack(ciphertext, pattern):
    indexes_arr = helpers._find_indexes_of_repeated_sequences(ciphertext, SEQUENCE_LEN_SEEK)
    spacings = helpers._find_spacings(indexes_arr)
    top_factors = helpers._foreach_find_factors(spacings)[:NUM_TRY_FACTORS]
    for factor in top_factors:
        key = ''
        for substr in helpers._build_every_nth_substr(ciphertext, factor):
            key += helpers._bruteforce_subkey(substr, pattern)
        if len(key) == factor:
            return key
    return ''

if __name__ == "__main__":
    ct = ''
    with open('text/ciphertext', 'rb') as f:
        ct = f.read().decode(ENCODING)
    key = hack(ct, PATTERN)
    print("key:", key)
    plaintext = decrypt_hex(ct, key)
    with open('text/plaintext', 'w') as f:
        f.write(plaintext)
