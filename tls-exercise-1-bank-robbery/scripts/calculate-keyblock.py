#!/usr/bin/env python3

import binascii
from prf import tls_prf

length_key_block = 2 * 20 + 2 * 16
master_secret = 'fee43619219b66e3a8651fcf3ca7380cea8378d76a5c0762293d2078f2746d76e4e0e8954e0d75beb9c4f33e6b27700f'
secret = binascii.unhexlify(master_secret)
label = 'key expansion'
client_random = '41f023c160b420bb3851d9d47acb933dbe70399bf6c92da33af01d4fb770e98c'
server_random = '41f023fa60b420bb3851d9d47acb933dbe70399bf6c92da33af01d4fb770e98c'
seed = binascii.unhexlify(server_random + client_random)
key_block = tls_prf(secret, label, seed, length_key_block)

print(key_block.hex())
