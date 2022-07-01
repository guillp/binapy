import hashlib

from binapy import binapy_checker, binapy_encoder


@binapy_encoder("shake128")
def hash_shake128(bp: bytes, length: int = 256) -> bytes:
    if length % 8:
        raise ValueError(
            "Shake-128 hash length is a number of bits and must be a multiple of 8"
        )
    return hashlib.shake_128(bp).digest(length // 8)
