#!/usr/bin/env python3

# Example of a weak hash implementation.
# It's a parity-like hash. The byte yi is the sum of xi of each word.
# Second preimage resistance and/or one-wayness is not ensured.

import sys
import functools
from typing import List

def compute_parity_hash(plaintext: str) -> int:
  binary_strings: List[str] = []
  for character in plaintext:
    binary_string: str = "{0:b}".format(ord(character)).rjust(8, '0')
    binary_strings.append(binary_string)
  hash_binary: str = ''
  for i in range(8):
    bytes_at_position_i: List[str] = [binary_string[i] for binary_string in binary_strings]
    hash_binary += functools.reduce(lambda a, b: str(int(a) ^ int(b)), bytes_at_position_i, '0')
  return hash_binary

plaintexts: List[str] = ['#CyB3R§', 'C#YB3R§', '"Byb3R§', 'C#yB3R$', \
    'C#yB3r§', 'Cyb3R§#', 'B#y3BU§', 'CyB3R§', '"Byb3r§']

for plaintext in plaintexts:
  hash_value: int = compute_parity_hash(plaintext)
  print(f'plaintext: {plaintext},\thash: {hash_value}\t({hex(int(hash_value, 2))})')
