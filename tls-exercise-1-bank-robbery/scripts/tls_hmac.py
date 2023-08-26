import hmac
import hashlib
import binascii

key = binascii.unhexlify('1234567890')
hmac_input = binascii.unhexlify('0987654321')
h = hmac.new(key,hmac_input, hashlib.sha256)
hmac_output = h.digest()
print(hmac_output.hex()) 
