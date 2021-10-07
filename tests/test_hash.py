from binapy import BinaPy


def test_hashes():
    bp = BinaPy("my_data")
    salt = BinaPy(b"my_salt")

    sha1 = bp.hash_sha1()
    assert sha1.is_sha1()
    assert sha1.encode_hex() == b"ab0c15b6029fdffce16b393f2d27ca839a76249e"
    ssha1 = bp.hash_ssha1(salt) + salt
    assert ssha1.is_ssha1()
    assert (
        ssha1.encode_hex() == b"1a02b81d432680616118dde7871df320dd9cab596d795f73616c74"
    )
    ssha1_prefix = salt + bp.hash_ssha1(salt, False)
    assert ssha1_prefix.is_ssha1()
    assert (
        ssha1_prefix.encode_hex()
        == b"6d795f73616c7474f3688c6f4f857a74d42e9541d8525072369742"
    )

    sha256 = bp.hash_sha256()
    assert sha256.is_sha256()
    assert (
        sha256.encode_hex()
        == b"e1f40338f64b974ab38d8711d51d8e848611aa8ca9f8d4dfdad0a61c30a77aac"
    )
    ssha256 = bp.hash_ssha256(salt) + salt
    assert ssha256.is_ssha256()
    assert (
        ssha256.encode_hex()
        == b"62a586524300d893af4caedd591d6eb9ba3127538e094972132c70e4d8ce1e516d795f73616c74"
    )
    ssha256_prefix = salt + bp.hash_ssha256(salt, False)
    assert ssha256_prefix.is_ssha256()
    assert (
        ssha256_prefix.encode_hex()
        == b"6d795f73616c7416e5ac5e0fff394792e38bc547054089188799fe26ab05c0c32d690fd5f991c4"
    )

    sha384 = bp.hash_sha384()
    assert sha384.is_sha384()
    assert (
        sha384.encode_hex()
        == b"d197041120319513ab5f91c293c391d8a2d5864bda581a144a1c7985a8d45bf24e2c2cef4a27b1bb20ddbef22a9e8723"
    )
    ssha384 = bp.hash_ssha384(salt) + salt
    assert ssha384.is_ssha384()
    assert (
        ssha384.encode_hex()
        == b"4e0a9be78865d599689c7d520cfb904347c822251e197db8062c638c0bf9da10ba1fe8573f2e7a57a2aeccc0df17addb6d795f73616c74"
    )
    ssha384_prefix = salt + bp.hash_ssha384(salt, False)
    assert ssha384_prefix.is_ssha384()
    assert (
        ssha384_prefix.encode_hex()
        == b"6d795f73616c74b52c3ec59e837033a4c336e521476570bf10203a22c381b4df6bc7789a2f1be57df9d21a64185b9cd54eabf216543104"
    )

    sha512 = bp.hash_sha512()
    assert sha512.is_sha512()
    assert (
        sha512.encode_hex()
        == b"c724e3e3ae93976abfe118e5a3b4aec6df4fe6beedc25aa53b085b39a186675238a5e25243d8e735e335f64b5905fdeeb1fec7d7ad971317a08af23a642ab669"
    )
    ssha512 = bp.hash_ssha512(salt) + salt
    assert ssha512.is_ssha512()
    assert (
        ssha512.encode_hex()
        == b"45ec2bde98ac821f0b5b663da25382b59ed7065aba77c73b37066e3f0523601474c727ebc85a97a652d55a6c342cba96030f84587078ac7a0cbf06c5f819c4c76d795f73616c74"
    )
    ssha512_prefix = salt + bp.hash_ssha512(salt, False)
    assert ssha512_prefix.is_ssha512()
    assert (
        ssha512_prefix.encode_hex()
        == b"6d795f73616c74cce5acf40a1d921ca6b3bdb1cc3136ff941f81d9207f57e80329633668086eb858c4de70ccd82ec93e42d75c2d63c8cae081ec4a1599bce9809626404e7e9f31"
    )
