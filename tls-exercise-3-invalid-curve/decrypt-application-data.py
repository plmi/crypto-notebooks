#!/usr/bin/env python3

import binascii
from Crypto.Cipher import AES


def decrypt_with_aes_cbc(iv, key, cipherblock):
    aes = AES.new(key, AES.MODE_CBC, IV=iv)
    plaintext = aes.decrypt(cipherblock)
    return binascii.hexlify(plaintext)


client_write_key = binascii.unhexlify('38fdd4483d8e4d4ba1736f0cb4cf1b5c')
iv = binascii.unhexlify('4bf0b54023c29b624de9ef9c2f931efc')
ciphertext = binascii.unhexlify('3c4e35927878ad451c2bded9bb5b76d3cc124b249cd9ed035904f7386d2192b643cbfefa1e1d0b6ccf49fc8760169f760a65c640cb4353df8277c8532f9bca8c968fda40b3f69aa562685ab61549b7a21be2d2f266fe365d93f8021381ab0bf6')
plaintext_bytes = decrypt_with_aes_cbc(iv, client_write_key, ciphertext)
# remove mac + padding
plaintext_bytes = plaintext_bytes[:len(plaintext_bytes) - 7 * 2 - 20 * 2]
print(binascii.unhexlify(plaintext_bytes).decode('ascii'))
