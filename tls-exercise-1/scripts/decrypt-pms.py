#!/usr/bin/env python3

import math


def decrypt_rsa(ciphertext, private_key, modulus):
    return pow(ciphertext, private_key, modulus)


private_key = 0x5ff49f4cc5c9b28ec671636534544f751973d62ec44735be0a41eec93121edcd3a4568c7f5ff65fadd60d9dd6bb242e009c08862b84ec5779ed3f5b4b3347b561a1287835352306dc8f8dfffd93d3795e93ad742c5839fb7d3f09f632a538d1a59869ad384a8dfceadf49be2a5d17c848125057f880080b46ddb5bba827e6c01

ciphertext = 0x484817070083d39006630d5727642d49a884a92b642288f940b784c3cc5e888f8b3cda45b44bc54a928708996943c466e056c6419f8faa31861d962cd3c6d0f2bacbf8e02c86efd71667f1ecc7854c6a328511994ac20e0a957a196a15ca1b63433444299d87ac4b40b5c66f2408f5bec92bbd88a5ac9455a85826d5c4dc1023

modulus = 0x00c119381ce79091b5c16a0c3459a7d1192b57ef5b11ee1bf2629ecf780a5679a95c17e39e2befb660eae84f490bd3eff36576784f6e1de680bec2b6d46b62fe8a9c41c54e544fc657352601a37571fd3e963f22ae92f86a605754f74252296f02e85f19d043ef3cfee00757dd97836fc969a948f54a6a17873eac2df604499111

plaintext = decrypt_rsa(ciphertext, private_key, modulus)
plaintext = hex(plaintext)[2:]
# strip last 48 bytes. this is the pms
pms = plaintext[len(plaintext) - 48 * 2:]
print(pms)
