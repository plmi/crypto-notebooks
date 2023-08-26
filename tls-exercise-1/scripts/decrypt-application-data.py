#!/usr/bin/env python3

import binascii
from Crypto.Cipher import AES


def decrypt_with_aes_cbc(iv, key, cipherblock):
    aes = AES.new(key, AES.MODE_CBC, IV=iv)
    plaintext = aes.decrypt(cipherblock)
    return binascii.hexlify(plaintext)


server_write_key = binascii.unhexlify('a7bf8900807f2bb494b8a66e3b4ae040')
iv = binascii.unhexlify('8b2879bd2716d24e5f8d9bb6bc7f1788')
ciphertext = binascii.unhexlify('446db7bde7e381981f7a370eb3e37a1fe93e9dcf7beff65b0b85d9920af59e2631a888a7e417515b675f0ddf5f7345720244d7c0357104d611d7bc568caad3cd4cadaacff908537412ab9c5c04010835')
plaintext_bytes = decrypt_with_aes_cbc(iv, server_write_key, ciphertext)
# remove mac + padding
plaintext_bytes = plaintext_bytes[:len(plaintext_bytes) - 7 * 2 - 20 * 2]
print(binascii.unhexlify(plaintext_bytes).decode('ascii'))
