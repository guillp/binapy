import hashlib

from binapy import binapy_checker, binapy_encoder


@binapy_encoder("sha1")
def hash_sha1(self):
    return hashlib.sha1(self).digest()


@binapy_checker("sha1")
def is_sha1(self):
    return len(self) == 20


@binapy_encoder("ssha1")
def hash_ssha1(self, salt, append=True):
    if append:
        salted = self + salt
    else:
        salted = salt + self
    return hashlib.sha1(salted).digest()


@binapy_checker("ssha1")
def is_ssha1(self):
    return 20 < len(self) < 40


@binapy_encoder("sha256")
def hash_sha256(self):
    return hashlib.sha256(self).digest()


@binapy_encoder("sha284")
def hash_sha384(self):
    return hashlib.sha384(self).digest()


@binapy_encoder("sha512")
def hash_sha512(self):
    return hashlib.sha512(self).digest()


@binapy_encoder("ssha256")
def hash_ssha256(self, salt, append=True):
    if append:
        salted = self + salt
    else:
        salted = salt + self
    return hashlib.sha256(salted).digest()
