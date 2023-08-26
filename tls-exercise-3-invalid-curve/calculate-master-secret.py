#!/usr/bin/env python3

import binascii
from prf import tls_prf

length_master_secret = 48
pms = '0e668af327265eb3fb7a0ce18be852e1961e64fb846d5f94f5b48b29362bd4a4'
secret = binascii.unhexlify(pms)
label = 'master secret'
client_random = '3b9b7d5e60b420bb3851d9d47acb933dbe70399bf6c92da33af01d4fb770e98c'
server_random = '6115674b0ad86ab4927dcb4abc0370af7aadcaf8220b75dd278082ee61c21f75'
seed = binascii.unhexlify(client_random + server_random)
master_secret = tls_prf(secret, label, seed, length_master_secret)

print(master_secret.hex())
