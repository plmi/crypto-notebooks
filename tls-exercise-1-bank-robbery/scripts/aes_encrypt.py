from Crypto.Cipher import AES
import binascii

key = binascii.unhexlify('1234')
IV = binascii.unhexlify(1234')
encryptor = AES.new(key, AES.MODE_CBC, IV=IV)
text = binascii.unhexlify('1234')
plaintext = encryptor.encrypt(text)
print(binascii.hexlify(plaintext).upper())
