import json
from typing import Any

from binapy import binapy_parser, binapy_serializer


@binapy_parser("json")
def to_json(bp: bytes) -> bytes:
    return json.loads(bp)


@binapy_serializer("json")
def from_json(data: Any, indent: int = 0) -> bytes:
    return json.dumps(data, indent=indent).encode()
