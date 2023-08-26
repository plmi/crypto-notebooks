from Crypto.Cipher import AES
import binascii

key = binascii.unhexlify('67d545b020c46aef2da4c1220380cde0')
IV = binascii.unhexlify('443020de1cad09bfd6381ffb94daafbb')
encryptor = AES.new(key, AES.MODE_CBC, IV=IV)
text = binascii.unhexlify('4576656e2074686520736d616c6c65737420706572736f6e2063616e206368616e67652074686520636f75727365206f6620746865206675747572652e4167a102881164829869b4633b0c59b462a651f66c367d0e1bc8db40dace705c020202')
ciphertext = encryptor.encrypt(text)
print(binascii.hexlify(ciphertext).upper().decode())
