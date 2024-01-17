"""Top-level package for BinaPy."""


from .binapy import (
    BinaPy,
    InvalidExtensionMethodError,
    binapy_checker,
    binapy_decoder,
    binapy_encoder,
    binapy_parser,
    binapy_serializer,
)

__all__ = [
    "BinaPy",
    "binapy_checker",
    "binapy_decoder",
    "binapy_encoder",
    "binapy_parser",
    "binapy_serializer",
    "InvalidExtensionMethodError",
]

from . import compression, encoding, hashing, parsing  # noqa: F401
