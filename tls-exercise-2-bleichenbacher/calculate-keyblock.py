#!/usr/bin/env python3

import binascii
from prf import tls_prf

length_key_block = 2 * 32 + 2 * 16 + 2 * 16
master_secret = 'b67cc1e784858f016119d120cd626d3f2429861e725da693432c8e710ad3bf53c7c2cdabc9a75beb6663e222c2c790ff'
secret = binascii.unhexlify(master_secret)
label = 'key expansion'
client_random = 'c111e13ad7249436640715c126decb2c8bcc94b7212002488af14a5e93786781'
server_random = '23fccc8f2fd92329371261bc96172cb8c9e55eea5a5524572bf7c4243bea5b52'
seed = binascii.unhexlify(server_random + client_random)
key_block = tls_prf(secret, label, seed, length_key_block)

print(key_block.hex())
