"""Main module."""
from __future__ import annotations

from functools import wraps
from typing import Any, Union


class BinaPy(bytes):
    """
    This is the only class that you will use to manipulate binary data.
    Since this is a bytes subclass, you can use instances of BinaPy anywhere you can use bytes.
    This provides a few helper methods compared to plain bytes.
    Actual transformations such as `encode_b64()` or `hash_sha256()` are implemented using Extensions.
    Those extensions are registered using the
    """

    def __new__(
        cls,
        value: Union[bytes, str] = b"",
        encoding: str = "utf-8",
        errors: str = "strict",
    ):
        """
        Overrides base method to accept a string with a default encoding of "utf-8".
        See Also:
            [`bytes` constructor](https://docs.python.org/3/library/stdtypes.html#bytes) and
            [`str.encode()`](https://docs.python.org/3/library/stdtypes.html#str.encode)
        Args:
            value: a `bytes` or a `str`
            encoding: if value is a `str`, specifies the encoding to use to encode this str to bytes
            errors: 'strict', 'ignore', 'replace', 'xmlcharrefreplace', or 'backslashreplace'
        """
        if isinstance(value, str):
            obj = bytes.__new__(cls, value, encoding=encoding, errors=errors)
        else:
            obj = bytes.__new__(cls, value)
        obj.encoding = encoding
        return obj

    @classmethod
    def from_int(
        cls, i: int, length: int = None, byteorder: str = "big", signed: bool = False
    ):
        """
        Converts an int to a BinaPy. This is a wrapper around
        [int.to_bytes()](https://docs.python.org/3/library/stdtypes.html#int.to_bytes) and takes
        the same parameters.
        Args:
            i: the integer to convert to BinaPy
            length: the length of the integer, in bytes. If omitted, takes the minimal length that fits the given integer.
            byteorder: "little" or "big" (defaults to "big")
            signed: determines whether two’s complement is used to represent the integer.

        Returns:
            a BinaPy with the binary representation of the given integer
        """

        if length is None:
            length = (i.bit_length() + 7) // 8

        data = i.to_bytes(length, byteorder, signed=signed)
        return cls(data)

    def __getitem__(self, index: int) -> BinaPy:
        """
        Overrides the base method so that slicing returns a BinaPy instead of just bytes.
        Args:
            index: an index

        Returns:
            A BinaPy
        """
        return self.__class__(super().__getitem__(index))

    def cut_at(self, *pos):
        """
        Cuts this BinaPy at one or more integer positions.
        Args:
            *pos: indexes where to cut the BinaPy

        Returns:
            `len(pos) + 1` parts, instances of BinaPy
        """
        spos = sorted(pos)
        return [
            self.__class__(self[start:end])
            for start, end in zip([0] + spos, spos + [len(self)])
        ]

    extensions = {}
    """
    Extension registry. New Extensions should be registered with `binapy_extension()`[binapy.binapy.binapy_extension].
    """

    def check(
        self, name: str, decode: bool = False, raise_on_error: bool = False
    ) -> (bool, Union[Any, Exception]):
        """
        Checks that this BinaPy conforms to a given extension format.
        Args:
            name: the name of the extension to check
            decode: if True, and the given extension doesn't have a checker method,
            try to decode this BinaPy using the decoder method  to check if that works.
            raise_on_error: if True, Exceptions from the checker method, if any, will be raised instead of returning False.

        Returns:
            a boolean, that is True if this BinaPy conforms to the given extension format, False otherwise.
        """
        extension = self.extensions.get(name)
        if extension is None:
            raise ValueError(f"Extension {name} not found")

        checker = extension.get("check", None)
        decoder = extension.get("decode", None)
        if checker:
            try:
                return checker(self)
            except Exception as exc:
                if raise_on_error:
                    raise exc from exc
                return False
        # if checker is not implemented and decode is True, try to decode instead
        if decode and decoder:
            try:
                decoder(self)
                return True
            except Exception as exc:
                if raise_on_error:
                    raise exc from exc
                return False

        return False

    def check_all(self, decode=False):
        """
        Checks if this BinaPy conforms to any of the registered extensions.
        Returns: a list of extensions that this BinaPy can be decoded from.

        Args:
            decode: if True, for extensions that don't have a checker method,
            try to decode this BinaPy using the decoder method to check if that works.
        """

        def get_results():
            for name in self.extensions:
                success = self.check(name, decode=decode)
                if success is True:
                    yield name

        return list(get_results())


def binapy_extension(name, encode=False, decode=False, check=False):
    """
    A decorator that will register extension methods for BinaPy.
    Each extension must have a name and at least one of:
    - an encoder method, that will transform data into the extension format
    - a decoder method, that will transform data from the extension format into a base format
    - a checker method, that will check if the data conforms to the extension format
    :param name: an extension name
    :param encode: set to True if this decorates an encoder method
    :param decode: set to True if this decorates a decoder method
    :param check: set to True if this decorates a checker method
    :return: the decorated method
    """

    if not (encode or decode or check):
        raise ValueError(
            "An extension must implement at least one of encode, decode or check"
        )

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            raw_result = func(*args, **kwargs)
            if encode or decode:
                return BinaPy(raw_result)
            else:
                return raw_result

        setattr(BinaPy, func.__name__, wrapper)
        BinaPy.extensions[name] = {}
        if encode:
            BinaPy.extensions[name]["encode"] = func
        if decode:
            BinaPy.extensions[name]["decode"] = func
        if check:
            BinaPy.extensions[name]["check"] = func
        return func

    return decorator
