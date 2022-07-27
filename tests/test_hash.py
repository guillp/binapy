from typing import Optional

import pytest

from binapy import BinaPy


@pytest.mark.parametrize(
    "alg, append_salt, hexhash",
    (
        ("sha1", None, "ab0c15b6029fdffce16b393f2d27ca839a76249e"),
        ("ssha1", True, "1a02b81d432680616118dde7871df320dd9cab59"),
        ("ssha1", False, "74f3688c6f4f857a74d42e9541d8525072369742"),
        (
            "sha256",
            None,
            "e1f40338f64b974ab38d8711d51d8e848611aa8ca9f8d4dfdad0a61c30a77aac",
        ),
        (
            "ssha256",
            True,
            "62a586524300d893af4caedd591d6eb9ba3127538e094972132c70e4d8ce1e51",
        ),
        (
            "ssha256",
            False,
            "16e5ac5e0fff394792e38bc547054089188799fe26ab05c0c32d690fd5f991c4",
        ),
        (
            "sha384",
            None,
            "d197041120319513ab5f91c293c391d8a2d5864bda581a144a1c7985a8d45bf24e2c2cef4a27b1bb20ddbef22a9e8723",
        ),
        (
            "ssha384",
            True,
            "4e0a9be78865d599689c7d520cfb904347c822251e197db8062c638c0bf9da10ba1fe8573f2e7a57a2aeccc0df17addb",
        ),
        (
            "ssha384",
            False,
            "b52c3ec59e837033a4c336e521476570bf10203a22c381b4df6bc7789a2f1be57df9d21a64185b9cd54eabf216543104",
        ),
        (
            "sha512",
            None,
            "c724e3e3ae93976abfe118e5a3b4aec6df4fe6beedc25aa53b085b39a186675238a5e25243d8e735e335f64b5905fdeeb1fec7d7ad971317a08af23a642ab669",
        ),
        (
            "ssha512",
            True,
            "45ec2bde98ac821f0b5b663da25382b59ed7065aba77c73b37066e3f0523601474c727ebc85a97a652d55a6c342cba96030f84587078ac7a0cbf06c5f819c4c7",
        ),
        (
            "ssha512",
            False,
            "cce5acf40a1d921ca6b3bdb1cc3136ff941f81d9207f57e80329633668086eb858c4de70ccd82ec93e42d75c2d63c8cae081ec4a1599bce9809626404e7e9f31",
        ),
    ),
)
def test_sha(alg: str, append_salt: Optional[bool], hexhash: str) -> None:
    data = BinaPy("my_data")
    salt = BinaPy(b"my_salt")

    if append_salt is None:
        bp = data.encode_to(alg)
    else:
        bp = data.encode_to(alg, salt, append_salt)

    assert bp.hex() == hexhash

    if append_salt is None:
        assert bp.check(alg)
    else:
        assert (bp + salt).check(alg)


@pytest.mark.parametrize(
    "alg, append_salt, length, hexhash",
    (
        (
            "shake128",
            None,
            256,
            "b0a8e0020f42c2a7302f817f64cacc432b9e4cb890349c1a3c443e0bc711bd30",
        ),
        (
            "shake256",
            None,
            512,
            "1f5f2f3e83df1a34a8a9525e92d0d10d1ee0da210ab445721f6c0684598a0f86dcd8d63c70f171ad1cf7b785ff044222f1165a5ebb307394e229d307aa0f419e",
        ),
        (
            "sshake128",
            True,
            256,
            "4a02381107dcafbe77c580c2e6b230e386575b426a116d41d2f43b4209de7e8c",
        ),
        (
            "sshake128",
            True,
            1024,
            "4a02381107dcafbe77c580c2e6b230e386575b426a116d41d2f43b4209de7e8c972dd3256091ffc825cddb3c02c330ec49a74d29ca28c6bde32a42a57050e2b2868c37a6548116ef9724821f1ede7527746b0493d313ac1592bc2b4b3bfafb6f73e77623e5ee2a9e40ae8ab4eea4e5b31f59f5f502ad9e5c7a922ab40da70b89",
        ),
        (
            "sshake256",
            True,
            512,
            "6025dc4128b18c52855dfcfbd40102236acabfa6d4958d49cb7cf0d4710f6b3daac7a73b357c6815a76c25aa631299be2d786b157dee4ddcd1c522a77c1edba1",
        ),
        (
            "sshake128",
            False,
            256,
            "4428a650cb7067900b518a2b7e45304131327f28450b81fd991a5f4eede853d5",
        ),
        (
            "sshake256",
            False,
            512,
            "5e1c64356ffe5f085da56b3570d249eff55425565dfa42320d37521c8bd8b707bf550d639675546cda872cb8435beb66e1b1b905795ccb9b78013fbe6e2fe1ea",
        ),
    ),
)
def test_shake(
    alg: str, append_salt: Optional[bool], length: int, hexhash: str
) -> None:
    data = BinaPy("my_data")
    salt = BinaPy(b"my_salt")

    if append_salt is None:
        bp = data.encode_to(alg, length)
    else:
        bp = data.encode_to(alg, length, salt, append_salt)
    assert bp.hex() == hexhash


def test_invalid_shake_length() -> None:
    with pytest.raises(ValueError):
        BinaPy("foo").to("shake128", 257)

    with pytest.raises(ValueError):
        BinaPy("foo").to("sshake128", 257, b"salt")
