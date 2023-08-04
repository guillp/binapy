from __future__ import annotations

import secrets

from binapy import BinaPy


class PickleTester:
    def __init__(self) -> None:
        self.random = secrets.token_hex()

    def __eq__(self, other: object) -> bool:
        return isinstance(other, PickleTester) and other.random == self.random


o = PickleTester()


def test_pickle() -> None:
    assert BinaPy.serialize_to("pickle", o).parse_from("pickle") == o
