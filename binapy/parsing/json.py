import json
from typing import Any

from binapy import binapy_parser, binapy_serializer


@binapy_parser("json")
def to_json(bp: bytes) -> bytes:
    return json.loads(bp)


@binapy_serializer("json")
def from_json(data: Any, compact: bool = True) -> bytes:
    if compact:
        separators = (",", ":")
        indent = None
    else:
        separators = (", ", ": ")
        indent = 2
    return json.dumps(data, separators=separators, indent=indent).encode()
