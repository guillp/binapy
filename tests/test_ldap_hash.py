import pytest

from binapy import BinaPy

PASSWORDS_HASHES = {"{SSHA}PdZrFYJugDAsBhR5U6OssLd+HSZ/JvYcDmSwCQ==": r"BzEuZ6vVRS"}


@pytest.fixture(params=PASSWORDS_HASHES.keys())
def ldap_password_hash(request):
    return request.param


@pytest.fixture
def password(ldap_password_hash):
    return PASSWORDS_HASHES.get(ldap_password_hash)


def test_ldap_password_hash(ldap_password_hash, password):
    bp = BinaPy(ldap_password_hash, encoding="UTF-8")
    if bp.startswith(b"{SHA}"):
        hash, salt = bp[5:].decode_b64().cut_at(20)
        assert BinaPy(password).hash_sha1(salt, append=True) == hash
    elif bp.startswith(b"{SSHA}"):
        hash, salt = bp[6:].decode_b64().cut_at(20)
        assert BinaPy(password).hash_ssha1(salt, append=True) == hash
    elif bp.startswith(b"{SHA256}"):
        hash, salt = bp[8:].decode_b64().cut_at(20)
        assert BinaPy(password).hash_sha256(salt, append=True) == hash
    elif bp.startswith(b"{SSHA256}"):
        hash, salt = bp[9:].decode_b64().cut_at(20)
        assert BinaPy(password).hash_ssha256(salt, append=True) == hash
    else:
        assert False, "unsupported hash type"
