#!/usr/bin/env python3

import binascii
from Crypto.Cipher import AES


def decrypt_with_aes_cbc(iv, key, cipherblock):
    aes = AES.new(key, AES.MODE_CBC, IV=iv)
    plaintext = aes.decrypt(cipherblock)
    return binascii.hexlify(plaintext)


with open('heartbleed.txt', 'rb') as file:
    content = file.read().rstrip(b'\n')

server_write_key = binascii.unhexlify('A113CAF95049C0C445E3F5B0702EA753')
iv = binascii.unhexlify(content[:32])
ciphertext = binascii.unhexlify(content[32:])
plaintext_bytes = decrypt_with_aes_cbc(iv, server_write_key, ciphertext)
# plaintext as bytes without mac | padding
# TYP | VERSION | LAENGE | (IV wenn >= TLS 1.1) | ENC(PLAINTEXT + MAC + PADDING)
plaintext = plaintext_bytes[:len(plaintext_bytes) - 2 * 5 - 2 * 20]
print(bytes.fromhex(plaintext.decode('ascii')).decode('utf-8', errors='ignore'))
