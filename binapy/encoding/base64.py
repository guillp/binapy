import base64
import string

from binapy.binapy import binapy_extension


@binapy_extension("b64", encode=True)
def encode_b64(self):
    return base64.b64encode(self)


@binapy_extension("b64", decode=True)
def decode_b64(self, strict=True):
    if strict and not is_b64(self):
        raise ValueError("not a base64")
    return base64.b64decode(self)


@binapy_extension("b64", check=True)
def is_b64(self):
    payload_len = len(self.rstrip(b"="))
    padding_size = payload_len % 4
    return set(self.rstrip(b"=")).issubset(
        bytes(string.ascii_letters + string.digits + "+/", encoding="ascii")
    ) and (
        padding_size == 0
        or (
            padding_size == 1
            and self.endswith(b"=")
            or (padding_size == 2)
            and self.endswith(b"==")
        )
    )


@binapy_extension("b64u", encode=True)
def encode_b64u(self):
    return base64.urlsafe_b64encode(self).rstrip(b"=")


@binapy_extension("b64u", decode=True)
def decode_b64u(self, strict=True):
    if strict and not is_b64u(self):
        raise ValueError("not a base64u")
    data = self
    padding_len = len(data) % 4
    if padding_len:
        data = data + b"=" * padding_len
    return base64.urlsafe_b64decode(data)


@binapy_extension("b64u", check=True)
def is_b64u(self):
    return set(self.rstrip(b"=")).issubset(
        bytes(string.ascii_letters + string.digits + "-_", encoding="ascii")
    )


@binapy_extension("b32", encode=True)
def encode_b32(self):
    return base64.b32encode(self)


@binapy_extension("b32", decode=True)
def decode_b32(self):
    return base64.b32decode(self)
