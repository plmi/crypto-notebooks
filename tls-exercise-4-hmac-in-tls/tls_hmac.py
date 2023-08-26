import hmac
import hashlib
import binascii

key = binascii.unhexlify('5f6fa4951a65884ab239d9af9b481874f6324df63bdca909a4bacdfe9c62f9ba')
hmac_input = binascii.unhexlify('0000000000000001170303003d4576656e2074686520736d616c6c65737420706572736f6e2063616e206368616e67652074686520636f75727365206f6620746865206675747572652e')
h = hmac.new(key, hmac_input, hashlib.sha256)
hmac_output = h.digest()
print(hmac_output.hex())
