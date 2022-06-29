import json
from datetime import datetime
from typing import Any, Callable

from binapy import binapy_parser, binapy_serializer


def _default_json_encode(data: Any) -> Any:
    if isinstance(data, datetime):
        return int(data.timestamp())
    return str(data)


@binapy_parser("json")
def to_json(bp: bytes) -> Any:
    return json.loads(bp)


@binapy_serializer("json")
def from_json(
    data: Any,
    compact: bool = True,
    default_encoder: Callable[[Any], Any] = _default_json_encode,
    **kwargs: Any
) -> bytes:
    if compact:
        kwargs.setdefault("separators", (",", ":"))
        kwargs.setdefault("indent", None)
    else:
        kwargs.setdefault("separators", (", ", ": "))
        kwargs.setdefault("indent", 2)
    return json.dumps(data, default=default_encoder, **kwargs).encode()
