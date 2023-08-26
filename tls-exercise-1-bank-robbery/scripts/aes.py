from Crypto.Cipher import AES
import binascii

key = binascii.unhexlify('11223344556677889900112233445566')
IV =  binascii.unhexlify('11223344556677889900112233445566')
decryptor = AES.new(key, AES.MODE_CBC, IV=IV)
text = binascii.unhexlify('11223344556677889900112233445566')
plaintext = decryptor.decrypt(text)
print(binascii.hexlify(plaintext).upper())
