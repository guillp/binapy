import string

import pytest

from binapy import BinaPy


@pytest.mark.parametrize("random", [BinaPy.random(length) for length in (40, 41, 42, 43)])
@pytest.mark.parametrize("encoding", ["b32", "b64", "b64u"])
def test_base64(random: BinaPy, encoding: str) -> None:
    # test multiple lengths to check for paddings
    assert random.encode_to(encoding).decode_from(encoding) == random


def test_invalid_b64() -> None:
    with pytest.raises(ValueError):
        BinaPy("a$5!)").decode_from("b64")
    with pytest.raises(ValueError):
        BinaPy("a$5!)").decode_from("b64u")


def test_hex() -> None:
    with pytest.raises(ValueError):
        BinaPy("aX123456").decode_from("hex")  # contains an X
    with pytest.raises(ValueError):
        BinaPy("a123456").decode_from("hex")  # odd number of chars

    random = BinaPy.random(39)
    assert random.encode_to("hex").decode_from("hex") == random


def test_url() -> None:
    bp = BinaPy("https://localhost:3200/foo?bar=ab cd")
    assert bp.encode_to("url").decode_from("url") == bp
    assert bp.encode_to("url") == b"https%3A//localhost%3A3200/foo%3Fbar%3Dab+cd"

    assert bp.encode_to("url", plus_spaces=False).decode_from("url", plus_spaces=False) == bp
    assert bp.encode_to("url", plus_spaces=False) == b"https%3A//localhost%3A3200/foo%3Fbar%3Dab%20cd"


def test_caesar() -> None:
    assert BinaPy("caesar13").to("caesar", 13, string.ascii_lowercase) == b"pnrfne13"
    assert BinaPy(string.ascii_lowercase).to("caesar", 13, string.ascii_lowercase) == b"nopqrstuvwxyzabcdefghijklm"
    assert (
        BinaPy(string.ascii_letters).to("caesar", 13, string.ascii_letters)
        == b"nopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklm"
    )

    for data in (b"caesar", b"CAESAR", b"FooBAR", bytes(range(128))):
        assert BinaPy(data).to("caesar", 4).decode_from("caesar", 4) == data

    assert BinaPy(b"\x00\xff").to("caesar", 1) == b"\x01\x00"
