#!/usr/bin/env python
"""Tests for `binapy` package."""

import pytest

from binapy.binapy import BinaPy

BINARY = b"\xd2m'\x10\x7f\xa9\xb0\xf4f\x9e\x85\xedBK%\x93"
BASE64 = b"0m0nEH+psPRmnoXtQkslkw=="
BASE64U = b"0m0nEH-psPRmnoXtQkslkw"
SHA256 = b"\x91\x02\xef\xd5U\xa6\xefr\xc9B\x18\x16\xa9\xf2\x8d\xf1Ur\x1d\xd1\x9en\xa0)\xf8\xb6\x0b\x93\x81\xce\xbc="


@pytest.fixture
def binary_sample():
    return BINARY


def test_binary(binary_sample):
    bp = BinaPy(binary_sample)
    assert len(bp) == 16
    b64 = bp.encode_b64()
    assert isinstance(b64, BinaPy)
    assert b64 == BASE64
    assert bp.encode_b64u() == BASE64U
    sha256 = bp.hash_sha256()
    assert isinstance(sha256, BinaPy)
    assert sha256 == SHA256
    assert bp.hash_sha256().encode_b64() == BinaPy(SHA256).encode_b64()
    assert isinstance(bp[:], BinaPy)
    assert isinstance(bp[4:-2], BinaPy)

    assert not bp.is_b64()
    assert BinaPy(BASE64).is_b64()

    assert not bp.check("b64")
    b64 = BinaPy(BASE64)
    assert b64.check("b64")

    extensions = b64.check_all()
    assert isinstance(extensions, list)
    for extension in extensions:
        assert extension in BinaPy.extensions
    assert "b64" in extensions

    assert b64.decode_from("b64") == BINARY
    assert bp.encode_to("b64") == b64


def test_helloworld():
    hello_world = "Hello, World!"
    bp = BinaPy(hello_world).compress_gzip().encode_b64u()
    assert bp == b"eJzzSM3JyddRCM8vyklRBAAfngRq"
    assert bp.decode_b64u().decompress_gzip().decode() == hello_world


def test_int():
    bp = BinaPy.from_int(0x12345678901234567890)
    assert bp == b"\x12\x34\x56\x78\x90\x12\x34\x56\x78\x90"

    bp = BinaPy.from_int(0x12345678901234567890, length=12)
    assert bp == b"\x00\x00\x12\x34\x56\x78\x90\x12\x34\x56\x78\x90"


def test_random():
    bp = BinaPy.random(12)
    assert len(bp) == 12
    assert bp != b"\00" * 12


def test_exceptions():
    bp = BinaPy.random(12)
    with pytest.raises(ValueError):
        bp.encode_to("something_not_known")

    with pytest.raises(ValueError):
        bp.decode_from("something_not_known")

    with pytest.raises(ValueError):
        bp.check("something_not_known")

    with pytest.raises(ValueError):
        bp.load("something_not_known")
