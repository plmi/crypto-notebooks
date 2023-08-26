import hashlib
import hmac


def _p_hash(secret, seed, output_length):
    result = bytearray()
    i = 1
    while len(result) < output_length:
        h = hmac.new(secret, b'', hashlib.sha256)
        h.update(_a(secret, hashlib.sha256, i, seed))
        h.update(seed)
        result.extend(h.digest())
        i += 1
    return bytes(result[:output_length])


def _a(secret, hash_algorithm, n, seed):
    if n == 0:
        return seed
    else:
        h = hmac.new(secret, b'', hash_algorithm)
        h.update(_a(secret, hash_algorithm, n - 1, seed))
        return h.digest()


def tls_prf(secret, label, seed, output_length):
    return _p_hash(secret, bytes(label, 'US-ASCII') + seed, output_length)
