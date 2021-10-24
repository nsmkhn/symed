# Symed
[Vigenere](https://en.wikipedia.org/wiki/Vigenère_cipher) implementation in Python.

## Encryption/Decryption Functions
1. Using [Tabula Recta](https://en.wikipedia.org/wiki/Tabula_recta)
```python
ciphertext = encrypt_tr(plaintext, keyword, tabula_recta(ALPHABET))
plaintext = decrypt_tr(ciphertext, keyword, tabula_recta(ALPHABET))
```

2. Algebraically
```python
ciphertext = encrypt_alg(plaintext, keyword, ALPHABET)
plaintext = decrypt_alg(ciphertext, keyword, ALPHABET)
```

3. Hex
```python
ciphertext = encrypt_hex(plaintext, keyword)
plaintext = decrypt_hex(ciphertext, keyword)
```
*Encryption/Decryption is done using byte-wise XOR*<br>
Why? Plaintext is not limited to alphabet(26 symbols) but ASCII character set.

## Decryption(Unknown Key)
[Kasiski Examination](https://pages.mtu.edu/~shene/NSF-4/Tutorial/VIG/Vig-Kasiski.html) implementation.
```python
key = hack(ciphertext, pattern)
decrypt_hex(ciphertext, key)
```
