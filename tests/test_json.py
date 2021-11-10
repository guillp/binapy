from binapy import BinaPy


def test_json():
    bp = BinaPy.from_json({"hello": "world"}).encode_b64()
    assert bp == b"eyJoZWxsbyI6IndvcmxkIn0="
    data = bp.decode_b64().to_json()
    assert data == {"hello": "world"}
