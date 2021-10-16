# Symed
## [Vigenere](https://en.wikipedia.org/wiki/Vigenère_cipher) Encyption/Decryption when key is known
1. Utilizing [Tabula Recta](https://en.wikipedia.org/wiki/Tabula_recta)
```
ciphertext = encrypt_tr(plaintext, keyword, tabula_recta(ALPHABET))
plaintext = decrypt_tr(ciphertext, keyword, tabula_recta(ALPHABET))
```
2. Algebraically<br>
> ciphertext[i] = (plaintext[i] + key[i]) mod ALPHABET_LEN<br>
> plaintext[i] = (ciphertext[i] - key[i] - ALPHABET_LEN) mod ALPHABET_LEN
```
ciphertext = encrypt_alg(plaintext, keyword, ALPHABET)
plaintext = decrypt_alg(ciphertext, keyword, ALPHABET)
```
3. Assuming ASCII plaintext<br>
```
ciphertext = encrypt_hex(plaintext, keyword)
plaintext = decrypt_hex(ciphertext, keyword)
```
*Encryption/Decryption is done using byte-wise XOR*<br>
Why? Plaintext is not limited to alphabet(26 symbols) but ASCII character set
## Hacking
Vigenere cryptoanalysis using [Kasiski Examination](https://pages.mtu.edu/~shene/NSF-4/Tutorial/VIG/Vig-Kasiski.html)
```
# pattern: RegEx describing which characters to consider valid in a plaintext
key = hack(ciphertext, pattern)
decrypt_hex(ciphertext, key)
```
