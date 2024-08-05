#!/usr/bin/env python
"""Tests for `binapy` package."""
import string

import pytest

from binapy import (
    BinaPy,
    InvalidExtensionMethodError,
    binapy_checker,
    binapy_decoder,
    binapy_encoder,
    binapy_serializer,
)

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
    assert bp.to("sha256").to("b64") == BinaPy(SHA256).to("b64")
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

    assert BinaPy("0123456789").split_at(3,5,8) == (b"012", b"34", b"567", b'89')
    assert BinaPy("0123456789").split_every(4) == (b"0123", b"4567", b"89")
    assert BinaPy("0123456789").split_every(12) == (b"0123456789",)
    assert BinaPy("0123456789").split_every(4, filler=b' ') == (b"0123", b"4567", b"89  ")

    assert BinaPy("0123456789").transpose(3) == b"0369147258"
    assert BinaPy("0123456789").transpose(3, filler=b' ') == b"0369147 258 "

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
    bp = BinaPy(hello_world).encode_to("zlib").encode_to("b64u")
    assert bp == b"eJzzSM3JyddRCM8vyklRBAAfngRq"
    assert bp.decode_from("b64u").decode_from("zlib") == hello_world


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

    bp = BinaPy.random_bits(192)
    assert len(bp) == 192 // 8
    assert bp != b"\00" * 24


def test_unknown_features() -> None:
    bp = BinaPy.random(12)
    with pytest.raises(NotImplementedError):
        bp.encode_to("something_not_known")

    with pytest.raises(NotImplementedError):
        bp.decode_from("something_not_known")

    with pytest.raises(NotImplementedError):
        bp.check("something_not_known")

    with pytest.raises(NotImplementedError):
        bp.parse_from("something_not_known")

    with pytest.raises(NotImplementedError):
        BinaPy.serialize_to("something_not_known", {"foo": "bar"})

    @binapy_encoder("something_known")
    def encode_something(bp: bytes) -> bytes:
        return bp

    with pytest.raises(NotImplementedError, match="Extension 'something_known' does not have a decode method"):
        bp.decode_from("something_known")

    with pytest.raises(NotImplementedError, match="Extension 'something_known' does not have a parse method"):
        bp.parse_from("something_known")

    with pytest.raises(NotImplementedError, match="Extension 'something_known' does not have a serialize method"):
        bp.serialize_to("something_known")

    with pytest.raises(NotImplementedError, match="Extension 'something_known' does not have a checker method"):
        bp.check("something_known")

    @binapy_decoder("something_else")
    def decode_something_else(bp: bytes) -> bytes:
        return bp

    with pytest.raises(NotImplementedError, match="Extension 'something_else' does not have an encode method"):
        bp.encode_to("something_else")



def test_exceptions() -> None:
    @binapy_decoder("some_feature")
    def decode_some_feature(bp: BinaPy) -> BinaPy:
        return bp

    bp = BinaPy()

    with pytest.raises(NotImplementedError):
        bp.check("some_feature")
    assert bp.check("some_feature", decode=True) is True

    @binapy_decoder("other_feature")
    def check_other_feature(bp: BinaPy) -> bool:
        raise ValueError()

    bp = BinaPy()
    with pytest.raises(NotImplementedError):
        bp.check("other_feature")
    assert bp.check("other_feature", decode=True) is False

    with pytest.raises(ValueError):
        bp.check("other_feature", decode=True, raise_on_error=True)

    with pytest.raises(NotImplementedError):
        bp.encode_to("other_feature", "foo")

    with pytest.raises(NotImplementedError):
        bp.parse_from("other_feature", "foo")

    with pytest.raises(NotImplementedError):
        bp.serialize_to("other_feature", "foo")

    with pytest.raises(NotImplementedError):
        bp.parse_from("other_feature", "foo")


def test_str() -> None:
    ascii_safe_chars = (
        "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
    )
    assert BinaPy(ascii_safe_chars, "ascii").ascii() == ascii_safe_chars

    assert BinaPy(string.ascii_letters + string.digits).re_match(r"[a-zA-Z0-9]")

    with pytest.raises(ValueError):
        BinaPy(b"\x01").text()

    with pytest.raises(ValueError):
        BinaPy(b"noturlsafe/").urlsafe()

    with pytest.raises(ValueError):
        BinaPy("notalphanumeric!").alphanumeric()


def test_binary_string() -> None:
    assert (
        BinaPy.from_binary_string(
            "01110100 01101000 01101001 01110011 00100000 01101001 01110011 00100000 01100001 00100000 01110100 01100101 01110011 01110100"
        )
        == b"this is a test"
    )
    assert (
        BinaPy(b"this is a test").to_binary_string()
        == "0111010001101000011010010111001100100000011010010111001100100000011000010010000001110100011001010111001101110100"
    )
    assert (
        BinaPy(b"this is a test").to_binary_string(pad=False)
        == "111010001101000011010010111001100100000011010010111001100100000011000010010000001110100011001010111001101110100"
    )


def test_invalid_features() -> None:
    @binapy_decoder("foo")
    def decode(bp: BinaPy) -> BinaPy:
        return 1  # type: ignore[return-value]

    with pytest.raises(InvalidExtensionMethodError):
        BinaPy("foo").decode_from("foo")

    @binapy_encoder("foo")
    def encode(bp: BinaPy) -> BinaPy:
        return 1  # type: ignore[return-value]

    with pytest.raises(InvalidExtensionMethodError):
        BinaPy("foo").to("foo")

    @binapy_checker("foo")
    def check(bp: BinaPy) -> BinaPy:
        return "whatever"  # type: ignore[return-value]

    with pytest.raises(InvalidExtensionMethodError):
        BinaPy("foo").check("foo")

    @binapy_serializer("foo")
    def serialize(bp: BinaPy) -> BinaPy:
        return 1  # type: ignore[return-value]

    with pytest.raises(InvalidExtensionMethodError):
        BinaPy.serialize_to("foo", "foo")

    @binapy_checker("foo")
    def check_with_exception(bp: BinaPy) -> BinaPy:
        raise ValueError()

    assert BinaPy("foo").check("foo") is False

    with pytest.raises(ValueError):
        assert BinaPy("foo").check("foo", raise_on_error=True)
