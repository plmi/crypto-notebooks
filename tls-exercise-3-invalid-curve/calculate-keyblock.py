#!/usr/bin/env python3

import binascii
from prf import tls_prf

length_key_block = 2 * 20 + 2 * 16
master_secret = '4f2114e25241e030e35e1829606194a720a8adf91e8c56ed66136cf80a3fc9e3d6773853e3097f1023b6a3adb758a973'
secret = binascii.unhexlify(master_secret)
label = 'key expansion'
client_random = '3b9b7d5e60b420bb3851d9d47acb933dbe70399bf6c92da33af01d4fb770e98c'
server_random = '6115674b0ad86ab4927dcb4abc0370af7aadcaf8220b75dd278082ee61c21f75'
seed = binascii.unhexlify(server_random + client_random)
key_block = tls_prf(secret, label, seed, length_key_block)

print(key_block.hex())
