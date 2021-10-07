import base64
import string

from binapy import binapy_checker, binapy_decoder, binapy_encoder


@binapy_encoder("b64")
def encode_b64(bp):
    return base64.b64encode(bp)


@binapy_decoder("b64")
def decode_b64(bp, strict=True):
    if strict and not is_b64(bp):
        raise ValueError("not a base64")
    return base64.b64decode(bp)


@binapy_checker("b64")
def is_b64(bp):
    payload_len = len(bp.rstrip(b"="))
    padding_size = 4 - (payload_len % 4)
    return set(bp.rstrip(b"=")).issubset(
        bytes(string.ascii_letters + string.digits + "+/", encoding="ascii")
    ) and (
        padding_size == 0
        or (
            padding_size == 1
            and bp.endswith(b"=")
            or (padding_size == 2)
            and bp.endswith(b"==")
        )
    )


@binapy_encoder("b64u")
def encode_b64u(bp):
    return base64.urlsafe_b64encode(bp).rstrip(b"=")


@binapy_decoder("b64u")
def decode_b64u(bp, strict=True):
    if strict and not is_b64u(bp):
        raise ValueError("not a base64u")
    data = bp
    padding_len = len(data) % 4
    if padding_len:
        data = data + b"=" * padding_len
    return base64.urlsafe_b64decode(data)


@binapy_checker("b64u")
def is_b64u(bp):
    return set(bp.rstrip(b"=")).issubset(
        bytes(string.ascii_letters + string.digits + "-_", encoding="ascii")
    )


@binapy_encoder("b32")
def encode_b32(bp):
    return base64.b32encode(bp)


@binapy_decoder("b32")
def decode_b32(bp):
    return base64.b32decode(bp)
