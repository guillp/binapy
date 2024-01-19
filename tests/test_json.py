import uuid
from collections import UserDict
from datetime import datetime, timedelta, timezone
from typing import Iterable

from binapy import BinaPy


def test_json() -> None:
    bp = BinaPy.serialize_to("json", {"hello": "world"}).encode_to("b64")
    assert bp == b"eyJoZWxsbyI6IndvcmxkIn0="
    data = bp.decode_from("b64").parse_from("json")
    assert data == {"hello": "world"}


def test_json_encoder() -> None:
    """Datetimes are serialized to integer epoch timestamps, but integer stay integers when
    parsed."""

    user_dict = UserDict({"my": "dict"})
    def iterable() -> Iterable[int]:
        for i in range(5):
            yield i

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
            "uuid": uuid.UUID("71509952-ec4f-4854-84e7-fa452994b51d"),
            "user_dict": user_dict,
            "iterable": iterable()
        },
        sort_keys=True,
    )
    assert bp == b'{"iat":1600000000,"iterable":[0,1,2,3,4],"user_dict":{"my":"dict"},"uuid":"71509952-ec4f-4854-84e7-fa452994b51d"}'

    assert bp.parse_from("json") == {
        "iat": 1600000000,
        "iterable": [0, 1, 2, 3, 4],
        "uuid": "71509952-ec4f-4854-84e7-fa452994b51d",
        "user_dict": {"my": "dict"}
    }


def test_compact() -> None:
    bp = BinaPy.serialize_to("json", {"a": "b", "c": "d"}, sort_keys=True, compact=True)
    assert bp == b'{"a":"b","c":"d"}'
    bp = BinaPy.serialize_to("json", {"a": "b", "c": "d"}, sort_keys=True, compact=False)
    assert bp == b'{\n  "a": "b", \n  "c": "d"\n}'

    bp = BinaPy.serialize_to("json", {"a": "b", "c": "d"}, sort_keys=True, compact=False, indent=4)
    assert bp == b'{\n    "a": "b", \n    "c": "d"\n}'
