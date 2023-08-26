#!/usr/bin/env python3

import binascii
from prf import tls_prf

length_master_secret = 48
pms = '0303e7d9d453c649d684b168428dc67cc46c7b68eb20584ecd9ce45c95d444a3074d646b7aafd991dfe1495f65b03fba'
secret = binascii.unhexlify(pms)
label = 'master secret'
client_random = 'c111e13ad7249436640715c126decb2c8bcc94b7212002488af14a5e93786781'
server_random = '23fccc8f2fd92329371261bc96172cb8c9e55eea5a5524572bf7c4243bea5b52'
seed = binascii.unhexlify(client_random + server_random)
master_secret = tls_prf(secret, label, seed, length_master_secret)

print(master_secret.hex())
