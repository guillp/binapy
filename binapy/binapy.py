"""Main module."""
from __future__ import annotations

import secrets
from functools import wraps
from typing import Any, Callable, Dict, List, Optional, Union


class BinaPy(bytes):
    """
    This is the only class that you will use to manipulate binary data.
    Since this is a bytes subclass, you can use instances of BinaPy anywhere you can use bytes.
    This provides a few helper methods compared to plain bytes.
    Actual transformations such as `encode_b64()` or `hash_sha256()` are implemented using Extensions.
    Those extensions are registered using the decorator `binapy_extension`.
    """

    def __new__(
        cls,
        value: Union[bytes, str] = b"",
        encoding: str = "utf-8",
        errors: str = "strict",
    ) -> BinaPy:
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
        return obj

    @classmethod
    def from_int(
        cls,
        i: int,
        length: Optional[int] = None,
        byteorder: str = "big",
        signed: bool = False,
    ) -> BinaPy:
        """
        Convert an `int` to a `BinaPy`. This is a wrapper around
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

    def to_int(self, byteorder: str = "big", signed: bool = False) -> int:
        """
        Convert this BinaPy to an `int`.

        This is a wrapper around
        [int.from_bytes()](https://docs.python.org/3/library/stdtypes.html#int.from_bytes) and takes
        the same parameters.
        Args:
            byteorder: "little" or "big" (defaults to "big")
            signed: determines whether two’s complement is used to represent the integer. Default to False.

        Returns:
            an integer based on this BinaPy binary value
        """
        return int.from_bytes(self, byteorder, signed=signed)

    @classmethod
    def random(cls, length: int) -> BinaPy:
        """
        Returns a BinaPy containing `length` random bytes
        Args:
            length:

        Returns:
            a BinaPy with randomly generated data
        """
        return cls(secrets.token_bytes(length))

    def __getitem__(self, index: slice) -> BinaPy:  # type: ignore
        """
        Overrides the base method so that slicing returns a BinaPy instead of just bytes.
        Args:
            index: an index

        Returns:
            A BinaPy
        """
        return self.__class__(super().__getitem__(index))

    def __add__(self, other: bytes) -> BinaPy:
        """
        Overrides base method so that addition returns a BinaPy instead of bytes.
        Args:
            other: bytes or BinaPy to add

        Returns:
            a BinaPy
        """
        return self.__class__(super().__add__(other))

    def __radd__(self, other: bytes) -> BinaPy:
        """
        Overrides base method so that right addition returns a BinaPy instead of bytes.
        Args:
            other: bytes or BinaPy to radd

        Returns:
            a BinaPy
        """
        return self.__class__(other.__add__(self))

    def cut_at(self, *pos: int) -> List[BinaPy]:
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

    extensions: Dict[str, Dict[str, Callable[..., Any]]] = {}
    """
    Extension registry. New Extensions should be registered with `binapy_extension()`[binapy.binapy.binapy_extension].
    """

    @classmethod
    def get_method(cls, extension_name: str, feature_name: str) -> Callable[..., Any]:
        extension_methods = cls.get_extension_methods(extension_name)
        method = extension_methods.get(feature_name)
        if method is None:
            raise ValueError(
                f"Extension {extension_name} doesn't have an {feature_name} method"
            )
        return method

    @classmethod
    def get_extension_methods(cls, name: str) -> Dict[str, Callable[..., Any]]:
        extension = cls.extensions.get(name)
        if extension is None:
            raise ValueError(f"Extension {name} not found")
        return extension

    def encode_to(self, name: str, *args: Any, **kwargs: Any) -> BinaPy:
        """
        Encodes data from this BinaPy according to the extension format `name`.
        Args:
            name: extension name to use
            *args: additional position parameters for the extension encoder method
            **kwargs: additional keyword parameters for the extension encoder method

        Returns:
            data as returned by the extension encoder method
        """
        encoder = self.get_method(name, "encode")

        return encoder(self, *args, **kwargs)

    def decode_from(self, name: str, *args: Any, **kwargs: Any) -> BinaPy:
        """
        Decodes data from this BinaPy according to the format `name`.
        Args:
            name: extension name to use
            *args: additional position parameters for the extension decoder method
            **kwargs: additional keyword parameters for the extension decoder method

        Returns:
            data as returned by the extension
        """
        decoder = self.get_method(name, "decode")

        return decoder(self, *args, **kwargs)

    def check(
        self, name: str, decode: bool = False, raise_on_error: bool = False
    ) -> bool:
        """
        Checks that this BinaPy conforms to a given extension format.
        Args:
            name: the name of the extension to check
            decode: if True, and the given extension doesn't have a checker method, try to decode this BinaPy using the decoder method  to check if that works.
            raise_on_error: if True, Exceptions from the checker method, if any, will be raised instead of returning False.

        Returns:
            a boolean, that is True if this BinaPy conforms to the given extension format, False otherwise.
        """

        # raises an exception in case the extension doesn't exist
        self.get_extension_methods(name)

        try:
            checker = self.get_method(name, "check")
            try:
                return checker(self)
            except Exception as exc:
                if raise_on_error:
                    raise exc from exc
                return False
        except ValueError:
            try:
                decoder = self.get_method(name, "decode")
                # if checker is not implemented and decode is True, try to decode instead
                if decode and decoder:
                    try:
                        decoder(self)
                        return True
                    except Exception as exc:
                        if raise_on_error:
                            raise exc from exc
                        return False
            except ValueError:
                return False
        return False

    def check_all(self, decode=False):
        """
        Checks if this BinaPy conforms to any of the registered extensions.
        Returns: a list of extensions that this BinaPy can be decoded from.

        Args:
            decode: if True, for extensions that don't have a checker method, try to decode this BinaPy using the decoder method to check if that works.
        """

        def get_results():
            for name in self.extensions:
                success = self.check(name, decode=decode)
                if success is True:
                    yield name

        return list(get_results())

    def parse_to(self, name: str, *args, **kwargs) -> Any:
        """
        Parse data from this BinaPy, based on a given extension format.
        Args:
            name: name of the extension to use
            *args: additional position parameters for the extension decoder method
            **kwargs: additional keyword parameters for the extension decoder method

        Returns:
            result from the extension loader method
        """
        parser = self.get_method(name, "parse")

        return parser(self, *args, **kwargs)

    @classmethod
    def serialize_from(cls, name: str, *args, **kwargs) -> BinaPy:
        """
        Dump data from this BinaPy, based on a given extension format.
        Args:
            name: name of the extension to use
            *args: additional position parameters for the extension decoder method
            **kwargs: additional keyword parameters for the extension decoder method

        Returns:
            result from the extension loader method
        """
        serializer = cls.get_method(name, "serialize")

        return serializer(*args, **kwargs)

    @classmethod
    def register_extension(
        cls, name: str, feature: str, func: Callable[..., Any]
    ) -> None:
        setattr(BinaPy, func.__name__, func)
        ext_dict = cls.extensions.setdefault(name, {})
        ext_dict[feature] = func


def binapy_encoder(name: str):
    def decorator(func: Callable[..., Any]):
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> BinaPy:
            raw_result = func(*args, **kwargs)
            if not isinstance(raw_result, (bytes, bytearray, str)):
                raise ValueError(
                    f"extension {name} encoder method did not return binary data"
                )
            return BinaPy(raw_result)

        BinaPy.register_extension(name, "encode", wrapper)
        return wrapper

    return decorator


def binapy_decoder(name: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            raw_result = func(*args, **kwargs)
            if not isinstance(raw_result, (bytes, bytearray)):
                raise ValueError(
                    f"extension {name} decoder method did not return binary data"
                )
            return BinaPy(raw_result)

        BinaPy.register_extension(name, "decode", wrapper)
        return wrapper

    return decorator


def binapy_checker(name: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            raw_result = func(*args, **kwargs)

            if not isinstance(raw_result, bool):
                raise ValueError(
                    f"extension {name} checker method did not return boolean data"
                )
            return raw_result

        BinaPy.register_extension(name, "check", wrapper)
        return wrapper

    return decorator


def binapy_serializer(name: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            raw_result = func(*args, **kwargs)
            if not isinstance(raw_result, (bytes, bytearray)):
                raise ValueError(
                    f"extension {name} serializer method did not return binary data"
                )
            return BinaPy(raw_result)

        BinaPy.register_extension(name, "serialize", wrapper)
        return wrapper

    return decorator


def binapy_parser(name: str):
    def decorator(func):
        BinaPy.register_extension(name, "parse", func)
        return func

    return decorator
