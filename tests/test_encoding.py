import pytest

from binapy import BinaPy


@pytest.fixture(params=(40, 41, 42, 43))
def random(request):
    return BinaPy.random(request.param)


def test_base64(random):
    # test multiple lengths to check for paddings
    assert random.encode_b64().decode_b64() == random
    assert random.encode_b64u().decode_b64u() == random
    assert random.encode_b32().decode_b32() == random


def test_invalid_b64():
    with pytest.raises(ValueError):
        BinaPy("a$5!)").decode_b64()
    with pytest.raises(ValueError):
        BinaPy("a$5!)").decode_b64u()


def test_hex():
    with pytest.raises(ValueError):
        BinaPy("aX123456").decode_hex()  # contains an X
    with pytest.raises(ValueError):
        BinaPy("a123456").decode_hex()  # odd number of chars

    random = BinaPy.random(39)
    assert random.encode_hex().decode_hex() == random


def test_url():
    bp = BinaPy("https://localhost:3200/foo?bar=ab cd")
    assert bp.url_encode().url_decode() == bp
    assert bp.url_encode() == b"https%3A//localhost%3A3200/foo%3Fbar%3Dab+cd"

    assert bp.url_encode(plus_spaces=False).url_decode(plus_spaces=False) == bp
    assert (
        bp.url_encode(plus_spaces=False)
        == b"https%3A//localhost%3A3200/foo%3Fbar%3Dab%20cd"
    )
