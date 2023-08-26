import eccFuncs
import sys
from collections import namedtuple
Point = namedtuple("Point", "x y")

if len(sys.argv) != 4:
    print("Usage: secp256r1.py [PubX] [PubY] [secret]")
else:
    x = int(sys.argv[1], 0)
    y = int(sys.argv[2], 0)
    scalar = int(sys.argv[3], 0)

    publicKey = Point(x, y)
    sharedSecret = eccFuncs.computeShared(publicKey, scalar)
    print("Computed Point: (" + str(sharedSecret.x) + "," + str(sharedSecret.y) + ")")
