#!/usr/bin/env python3

import binascii
from prf import tls_prf

length_master_secret = 48
pms = '0303495f614d5f676f696e475f746f5f64657374726f795f796f755f666f725f796f75725f73696e7300000000000000'
secret = binascii.unhexlify(pms)
label = 'master secret'
client_random = '41f023c160b420bb3851d9d47acb933dbe70399bf6c92da33af01d4fb770e98c'
server_random = '41f023fa60b420bb3851d9d47acb933dbe70399bf6c92da33af01d4fb770e98c'
seed = binascii.unhexlify(client_random + server_random)
master_secret = tls_prf(secret, label, seed, length_master_secret)

print(master_secret.hex())
