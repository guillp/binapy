from datetime import datetime, timedelta, timezone

from binapy import BinaPy


def test_json() -> None:
    bp = BinaPy.serialize_to("json", {"hello": "world"}).encode_to("b64")
    assert bp == b"eyJoZWxsbyI6IndvcmxkIn0="
    data = bp.decode_from("b64").parse_from("json")
    assert data == {"hello": "world"}


def test_json_datetime() -> None:
    """Datetimes are serialized to integer epoch timestamps, but integer stay integers when parsed."""
    bp = BinaPy.serialize_to(
        "json",
        {
            "iat": datetime(
                year=2020,
                month=9,
                day=13,
                hour=12,
                minute=26,
                second=40,
                tzinfo=timezone(timedelta(seconds=0)),
            )
        },
    )
    assert bp == b'{"iat":1600000000}'

    assert bp.parse_from("json") == {"iat": 1600000000}
