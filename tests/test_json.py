import uuid
from datetime import datetime, timedelta, timezone

from binapy import BinaPy


def test_json() -> None:
    bp = BinaPy.serialize_to("json", {"hello": "world"}).encode_to("b64")
    assert bp == b"eyJoZWxsbyI6IndvcmxkIn0="
    data = bp.decode_from("b64").parse_from("json")
    assert data == {"hello": "world"}


def test_json_encoder() -> None:
    """Datetimes are serialized to integer epoch timestamps, but integer stay integers when
    parsed."""
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
            ),
            "foo": uuid.UUID("71509952-ec4f-4854-84e7-fa452994b51d"),
        },
        sort_keys=True,
    )
    assert bp == b'{"foo":"71509952-ec4f-4854-84e7-fa452994b51d","iat":1600000000}'

    assert bp.parse_from("json") == {
        "iat": 1600000000,
        "foo": "71509952-ec4f-4854-84e7-fa452994b51d",
    }


def test_compact() -> None:
    bp = BinaPy.serialize_to("json", {"a": "b", "c": "d"}, sort_keys=True, compact=True)
    assert bp == b'{"a":"b","c":"d"}'
    bp = BinaPy.serialize_to(
        "json", {"a": "b", "c": "d"}, sort_keys=True, compact=False
    )
    assert bp == b'{\n  "a": "b", \n  "c": "d"\n}'

    bp = BinaPy.serialize_to(
        "json", {"a": "b", "c": "d"}, sort_keys=True, compact=False, indent=4
    )
    assert bp == b'{\n    "a": "b", \n    "c": "d"\n}'
