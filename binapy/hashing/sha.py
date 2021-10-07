import hashlib

from binapy import binapy_checker, binapy_encoder


@binapy_encoder("sha1")
def hash_sha1(bp: bytes) -> bytes:
    return hashlib.sha1(bp).digest()


@binapy_checker("sha1")
def is_sha1(bp: bytes) -> bool:
    return len(bp) == 20


@binapy_encoder("ssha1")
def hash_ssha1(bp: bytes, salt: bytes, append: bool = True) -> bytes:
    if append:
        salted = bp + salt
    else:
        salted = salt + bp
    return hashlib.sha1(salted).digest()


@binapy_checker("ssha1")
def is_ssha1(bp: bytes) -> bool:
    return 20 < len(bp) < 40


@binapy_encoder("sha256")
def hash_sha256(bp: bytes) -> bytes:
    return hashlib.sha256(bp).digest()


@binapy_checker("sha256")
def is_sha256(bp: bytes) -> bool:
    return len(bp) == 256 / 8


@binapy_encoder("sha384")
def hash_sha384(bp: bytes) -> bytes:
    return hashlib.sha384(bp).digest()


@binapy_checker("sha384")
def is_sha384(bp: bytes) -> bool:
    return len(bp) == 384 / 8


@binapy_encoder("sha512")
def hash_sha512(bp: bytes) -> bytes:
    return hashlib.sha512(bp).digest()


@binapy_checker("sha512")
def is_sha512(bp: bytes) -> bool:
    return len(bp) == 512 / 8


@binapy_encoder("ssha256")
def hash_ssha256(bp: bytes, salt: bytes, append: bool = True) -> bytes:
    if append:
        salted = bp + salt
    else:
        salted = salt + bp
    return hashlib.sha256(salted).digest()


@binapy_checker("ssha256")
def is_ssha256(bp: bytes) -> bool:
    return 32 < len(bp) < 64


@binapy_encoder("ssha384")
def hash_ssha384(bp: bytes, salt: bytes, append: bool = True) -> bytes:
    if append:
        salted = bp + salt
    else:
        salted = salt + bp
    return hashlib.sha384(salted).digest()


@binapy_checker("ssha384")
def is_ssha384(bp: bytes) -> bool:
    return 48 < len(bp) < 96


@binapy_encoder("ssha512")
def hash_ssha512(bp: bytes, salt: bytes, append: bool = True) -> bytes:
    if append:
        salted = bp + salt
    else:
        salted = salt + bp
    return hashlib.sha512(salted).digest()


@binapy_checker("ssha512")
def is_ssha512(bp: bytes) -> bool:
    return 64 < len(bp) < 128
