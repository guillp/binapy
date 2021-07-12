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


def test_binapy(binary_sample):
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
    assert BinaPy(BASE64).check("b64")

    extensions = BinaPy(BASE64).check_all()
    assert isinstance(extensions, list)
    for extension in extensions:
        assert extension in BinaPy.extensions
    assert "b64" in extensions


def test_helloworld():
    hello_world = "Hello, World!"
    bp = BinaPy(hello_world).compress_gzip().encode_b64u()
    assert bp == b"eJzzSM3JyddRCM8vyklRBAAfngRq"
    assert bp.decode_b64u().decompress_gzip().decode() == hello_world
