import pytest

from binapy import BinaPy


@pytest.mark.parametrize(
    "ldap_password_hash, hashing, hash_size, password",
    (
        (b"{SSHA}PdZrFYJugDAsBhR5U6OssLd+HSZ/JvYcDmSwCQ==", "ssha1", 20, r"BzEuZ6vVRS"),
        (
            b"{SSHA512}ZGdo6Ebqtsts554kedXUeO77GwnVexnl89SdA6cWgjOw4o+3EwzFAi7XJReFcG7xqLSDasj05qw8wuSjIcpgi0XlGAlSRg67",
            "ssha512",
            64,
            "changeme",
        ),
    ),
)
def test_validate_ldap_password_hash(
    ldap_password_hash: bytes, hashing: str, hash_size: int, password: str
) -> None:
    bp = BinaPy(ldap_password_hash)
    header, hash_with_salt = bp.split(b"}", 1)
    hash, salt = hash_with_salt.decode_from("b64").cut_at(hash_size)
    assert BinaPy(password).encode_to(hashing, salt, append=True) == hash
