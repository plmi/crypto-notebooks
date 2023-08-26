#!/usr/bin/env python3

import binascii
from Crypto.Cipher import AES


def decrypt_with_aes_cbc(iv, key, cipherblock):
    aes = AES.new(key, AES.MODE_CBC, IV=iv)
    plaintext = aes.decrypt(cipherblock)
    return binascii.hexlify(plaintext)


server_write_key = 'A1#CAF95049C0C445E3F5B0702EA753'
iv = binascii.unhexlify('0325f41d3ebaf8986da712c82bcd4d55')
ciphertext = binascii.unhexlify('aaddd1962606637f0bb7e8c9c9e1efa'
                                + '66e2ca9043af3f95b1b870a3d4574'
                                + '31eadc6d665b7785bc96c47a0b60e'
                                + 'ec80c03')
for i in range(0, 256):
    guess: str = "0x{:02x}".format(i)[2:]
    key = binascii.unhexlify(server_write_key.replace('#', guess))
    plaintext = decrypt_with_aes_cbc(iv, key, ciphertext)
    print(guess + ': ' + plaintext.decode('ascii'))
    # 13: 1400000c8fef30a8aa6073e0b80593adf2699432eb2b3b005312373bfdde3953f4ef81a20b0b0b0b0b0b0b0b0b0b0b0b
