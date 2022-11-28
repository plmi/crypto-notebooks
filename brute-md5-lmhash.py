#!/usr/bin/env python3

import hashlib

"""
This is a bruteforce demonstration of simplified version of lm hash.
The 14 byte password consists of numbers only.
Instead of DES the implementation uses MD5 with only its first 8 bytes.
The password is salted but the salt is known to the attacker.
An attacker can test his/her implementation with an already known (password, constant) tuple.
"""

def md5(password, constant) -> str:
    m = hashlib.md5()
    m.update(str.encode(password + constant))
    return m.hexdigest()

def bruteforce_lm_hash(expected_digest: str, constant: str) -> str:
  """
  Break one-way function of weak custom hash implementation with a given constant
  The password must be numeric and always 7 byte long padded with zeros
  """
  for i in range(10**7):
    padded_password_candidate: str = str(i).ljust(7, '0')
    digest_candidate: str = md5(padded_password_candidate, constant)
    if digest_candidate[:16] == expected_digest:
      return padded_password_candidate
  raise ValueError(f'No valid password candiate found for {expected_digest}')

def bruteforce(lm_hash: str, constant: str) -> None:
  """
  Bruteforce password for a given lm hash and constant
  """
  lm_hash_part_1: str = lm_hash[:16]
  lm_hash_part_2: str = lm_hash[16:]
  password_candidate_part_1: str = bruteforce_lm_hash(lm_hash_part_1, constant)
  password_candidate_part_2: str = bruteforce_lm_hash(lm_hash_part_2, constant)
  return f'{password_candidate_part_1}{password_candidate_part_2}'.ljust(14, '0')

constant: str = 'NetSec1'
lm_hash: str = 'b749eabf45a456a5f1cd5a59ff93c6de'

# verify bruteforce algorithm by an already known (password, lm hash) tuple
assert bruteforce('c98484bc0ee0509fda498b1fe098c2c3', constant) == '22334455000000'

print(f'lm hash {lm_hash}, constant: {constant}')
password: str = bruteforce(lm_hash, constant)
print(f'password: {password}')
