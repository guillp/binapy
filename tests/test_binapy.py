#!/usr/bin/env python
"""Tests for `binapy` package."""

import pytest

from binapy import BinaPy, binapy_decoder

BINARY = b"\xd2m'\x10\x7f\xa9\xb0\xf4f\x9e\x85\xedBK%\x93"
BASE64 = b"0m0nEH+psPRmnoXtQkslkw=="
BASE64U = b"0m0nEH-psPRmnoXtQkslkw"
SHA256 = b"\x91\x02\xef\xd5U\xa6\xefr\xc9B\x18\x16\xa9\xf2\x8d\xf1Ur\x1d\xd1\x9en\xa0)\xf8\xb6\x0b\x93\x81\xce\xbc="
JSON = {"foo": "bar"}


def test_binapy() -> None:
    bp = BinaPy(BINARY)
    assert len(bp) == 16
    b64 = bp.encode_to("b64")
    assert isinstance(b64, BinaPy)
    assert b64 == BASE64
    assert bp.encode_to("b64u") == BASE64U
    sha256 = bp.encode_to("sha256")
    assert isinstance(sha256, BinaPy)
    assert sha256 == SHA256
    assert bp.encode_to("sha256").encode_to("b64") == BinaPy(SHA256).encode_to("b64")
    assert isinstance(bp[:], BinaPy)
    assert isinstance(bp[4:-2], BinaPy)
    assert bp.encode_to("b64u").ascii() == "0m0nEH-psPRmnoXtQkslkw"
    with pytest.raises(UnicodeError):
        assert bp.ascii()

    assert not bp.check("b64")
    assert BinaPy(BASE64).check("b64")

    b64 = BinaPy(BASE64)
    assert b64.check("b64")

    extensions = b64.check_all()
    assert isinstance(extensions, list)
    for extension in extensions:
        assert extension in BinaPy.extensions
    assert "b64" in extensions

    assert b64.decode_from("b64") == BINARY
    assert bp.encode_to("b64") == b64

    bp_add = BinaPy(b"123") + b"456"
    assert isinstance(bp_add, BinaPy)
    assert bp_add == BinaPy(b"123456")

    bp_radd = b"123" + BinaPy(b"456")
    assert isinstance(bp_radd, BinaPy)
    assert bp_radd == BinaPy(b"123456")

    assert BinaPy.serialize_to("json", JSON).parse_from("json") == JSON


def test_slicing() -> None:
    bp = BinaPy("1234567890")
    assert bp[0] == ord("1")
    assert bp[-1] == ord("0")
    assert bp.char_at(0) == "1"
    assert bp.char_at(-1) == "0"
    assert bp[:] == bp
    assert isinstance(bp[0], int)
    assert isinstance(bp[:], BinaPy)
    assert isinstance(bp.char_at(0), str)


def test_helloworld() -> None:
    hello_world = b"Hello, World!"
    bp = BinaPy(hello_world).encode_to("gzip").encode_to("b64u")
    assert bp == b"eJzzSM3JyddRCM8vyklRBAAfngRq"
    assert bp.decode_from("b64u").decode_from("gzip") == hello_world


def test_int() -> None:
    i = 0x12345678901234567890
    bp = BinaPy.from_int(i)
    assert bp == b"\x12\x34\x56\x78\x90\x12\x34\x56\x78\x90"
    assert bp.to_int() == i

    bp = BinaPy.from_int(i, length=12)
    assert bp == b"\x00\x00\x12\x34\x56\x78\x90\x12\x34\x56\x78\x90"
    assert bp.to_int() == i


def test_random() -> None:
    bp = BinaPy.random(12)
    assert len(bp) == 12
    assert bp != b"\00" * 12


def test_unknown_features() -> None:
    bp = BinaPy.random(12)
    with pytest.raises(ValueError):
        bp.encode_to("something_not_known")

    with pytest.raises(ValueError):
        bp.decode_from("something_not_known")

    with pytest.raises(ValueError):
        bp.check("something_not_known")

    with pytest.raises(ValueError):
        bp.parse_from("something_not_known")

    with pytest.raises(ValueError):
        BinaPy.serialize_to("something_not_known", {"foo": "bar"})


def test_exceptions() -> None:
    @binapy_decoder("some_feature")
    def decode_some_feature(bp: BinaPy) -> BinaPy:
        return bp

    bp = BinaPy()

    assert bp.check("some_feature") is False
    assert bp.check("some_feature", decode=True) is True

    @binapy_decoder("other_feature")
    def check_other_feature(bp: BinaPy) -> bool:
        raise ValueError()

    bp = BinaPy()
    assert bp.check("other_feature") is False
    assert bp.check("other_feature", decode=True) is False
