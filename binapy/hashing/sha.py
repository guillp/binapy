import hashlib

from binapy import binapy_extension


@binapy_extension("sha1", encode=True)
def hash_sha1(self):
    return hashlib.sha1(self).digest()


@binapy_extension("sha1", check=True)
def is_sha1(self):
    return len(self) == 20


@binapy_extension("ssha1", encode=True)
def hash_ssha1(self, salt, append=True):
    if append:
        salted = self + salt
    else:
        salted = salt + self
    return hashlib.sha1(salted).digest()


@binapy_extension("ssha1", check=True)
def is_ssha1(self):
    return 20 < len(self) < 40


@binapy_extension("sha256", encode=True)
def hash_sha256(self):
    return hashlib.sha256(self).digest()


@binapy_extension("sha284", encode=True)
def hash_sha384(self):
    return hashlib.sha384(self).digest()


@binapy_extension("sha512", encode=True)
def hash_sha512(self):
    return hashlib.sha512(self).digest()


@binapy_extension("ssha256", encode=True)
def hash_ssha256(self, salt, append=True):
    if append:
        salted = self + salt
    else:
        salted = salt + self
    return hashlib.sha256(salted).digest()
