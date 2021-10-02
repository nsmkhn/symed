ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

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
        ciphertext += alphabet[((ord(letter) + ord(key[i])) % len(alphabet))]
    return ciphertext

def decrypt_alg(ciphertext, keyword, alphabet):
    key = keyword * (len(ciphertext) // len(keyword) + 1)
    plaintext = ''
    for i, letter in enumerate(ciphertext):
        plaintext += alphabet[(ord(letter) - ord(key[i]) + len(alphabet)) % len(alphabet)]
    return plaintext

def hack(ciphertext):
    pass

ct = encrypt_tr('ATTACKATDAWN', 'LEMON', TABULA_RECTA)
print("Ciphertext: ", ct)
ct = encrypt_alg('ATTACKATDAWN', 'LEMON', ALPHABET)
print("Ciphertext: ", ct)
print("Plaintext: ", decrypt_tr(ct, 'LEMON', TABULA_RECTA))
print("Plaintext: ", decrypt_alg(ct, 'LEMON', ALPHABET))
