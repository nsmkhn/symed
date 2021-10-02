ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

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

def encrypt_alg(plaintext, keyword, alphabet):
    key = keyword * (len(plaintext) // len(keyword) + 1)
    ciphertext = ''
    for i, letter in enumerate(plaintext):
        ciphertext += alphabet[((alphabet.find(letter) + alphabet.find(key[i])) % len(alphabet))]
    return ciphertext

def encrypt_hex(plaintext, keyword):
    key = keyword * (len(plaintext) // len(keyword) + 1)
    plaintext_hex = ''.join(hex(ord(c))[2:] for c in plaintext)
    key_hex = ''.join(hex(ord(c))[2:] for c in key)
    ciphertext = bytearray()
    for i in range(0, len(plaintext_hex), 2):
        ciphertext += bytearray.fromhex(hex(int(plaintext_hex[i:i+2], 16) ^ int(key_hex[i:i+2], 16))[2:].zfill(2))
    return ciphertext.decode(encoding='ascii')

def decrypt_hex(ciphertext, keyword):
    key = keyword * (len(ciphertext) // len(keyword) + 1)
    ciphertext_hex = ''.join(hex(ord(c))[2:].zfill(2) for c in ciphertext)
    key_hex = ''.join(hex(ord(c))[2:] for c in key)
    plaintext = bytearray()
    for i in range(0, len(ciphertext_hex), 2):
        plaintext += bytearray.fromhex(hex(int(ciphertext_hex[i:i+2], 16) ^ int(key_hex[i:i+2], 16))[2:].zfill(2))
    return plaintext.decode(encoding='ascii')

def decrypt_tr(ciphertext, keyword, tr):
    key = keyword * (len(ciphertext) // len(keyword) + 1)
    plaintext =  ''
    for i, letter in enumerate(ciphertext):
        plaintext += list(tr[key[i]].keys())[list(tr[key[i]].values()).index(letter)]
    return plaintext

def decrypt_alg(ciphertext, keyword, alphabet):
    key = keyword * (len(ciphertext) // len(keyword) + 1)
    plaintext = ''
    for i, letter in enumerate(ciphertext):
        plaintext += alphabet[(alphabet.find(letter) - alphabet.find(key[i]) + len(alphabet)) % len(alphabet)]
    return plaintext

def hack(ciphertext):
    pass

ct = encrypt_tr('ATTACKATDAWN', 'LEMON', TABULA_RECTA)
print('Ciphertext:', ct)
print('Plaintext:', decrypt_tr(ct, 'LEMON', TABULA_RECTA))

ct = encrypt_alg('attackatdawn', 'LEMON', ALPHABET)
print('Ciphertext:', ct)
print('Plaintext:', decrypt_alg(ct, 'LEMON', ALPHABET))

ct = encrypt_hex('attackatdawn', 'LEMON')
print('Ciphertext:', ct)
print('Plaintext:', decrypt_hex(ct, 'LEMON'))
