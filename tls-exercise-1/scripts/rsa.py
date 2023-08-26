from math import log
def bytes_needed(n):
     if n == 0:
         return 1
     return int(log(n, 256)) + 1
privateKey = 0x1337
jiphertext = 0x1337
modulus = 0x1337
plaintext = pow(ciphertext,privateKey, modulus)
print('Decimal: ' + str(plaintext))
print('Hex: ' + format(plaintext, 'x').zfill(2*(bytes_needed(modulus))))
