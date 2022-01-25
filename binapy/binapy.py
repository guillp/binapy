"""Main module."""

import secrets
from functools import wraps
from typing import (
    Any,
    Callable,
    Dict,
    Iterator,
    List,
    Literal,
    Optional,
    TypeVar,
    Union,
    cast,
    overload,
)


class BinaPy(bytes):
    """
    This is the only class that you will use to manipulate binary data.
    Since this is a bytes subclass, you can use instances of BinaPy anywhere you can use bytes.
    This provides a few helper methods compared to plain bytes.
    Actual transformations such as `encode_b64()` or `hash_sha256()` are implemented using Extensions.
    Those extensions are registered using the decorators `binapy_encoder`, `binapy_decoder`, `binapy_checker`,
    `binapy_serializer`, and `binapy_parser`.
    """

    def __new__(
        cls,
        value: Union[bytes, str] = b"",
        encoding: str = "utf-8",
        errors: str = "strict",
    ) -> "BinaPy":
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
        byteorder: Literal["little", "big"] = "big",
        signed: bool = False,
    ) -> "BinaPy":
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

    def ascii(self) -> str:
        """
        Convert this BinaPy to a str, making sure that only ascii characters are employed.
        Returns: a str
        """
        return self.decode("ascii")

    def to_int(
        self, byteorder: Literal["little", "big"] = "big", signed: bool = False
    ) -> int:
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
    def from_binary_string(
        cls, s: str, byteorder: Literal["little", "big"] = "big", signed: bool = False
    ) -> "BinaPy":
        """
        Initializes a BinaPy based on a binary string (containing only 0 and 1).

        Args:
            s: a binary string
            byteorder: byte order to use
            signed: True if 2 complement is used to represent negative values

        Returns:
            a BinaPy
        """
        return cls(
            int(s, 2).to_bytes((len(s) + 7) // 8, byteorder=byteorder, signed=signed)
        )

    def to_binary_string(
        self, byteorder: Literal["little", "big"] = "big", signed: bool = False
    ) -> str:
        """
        Returns a string containing this this BinaPy in binary representation.

        Args:
            byteorder: byte order to use
            signed: True if 2 complement is used to represent negative values
        Returns:
            a string with containing only 0 and 1
        """
        return f"{self.to_int(byteorder, signed):b}"

    @classmethod
    def random(cls, length: int) -> "BinaPy":
        """
        Return a BinaPy containing `length` random bytes
        Args:
            length:

        Returns:
            a BinaPy with randomly generated data
        """
        return cls(secrets.token_bytes(length))

    @overload
    def __getitem__(self, slice: int) -> int:
        ...

    @overload
    def __getitem__(self, slice: slice) -> "BinaPy":
        ...

    def __getitem__(self, slice: Union[int, slice]) -> "Union[int, BinaPy]":
        """
        Override the base method so that slicing returns a BinaPy instead of just bytes.
        Args:
            index: an index

        Returns:
            A BinaPy
        """
        if isinstance(slice, int):
            return super().__getitem__(slice)
        return self.__class__(super().__getitem__(slice))

    def char_at(self, index: int) -> str:
        """
        Return the character at the given index.

        Slicing a standard bytes returns an int. Sometimes what you really want is a single char string.
        Args:
            index:

        Returns:
            the single character at the given index
        """
        return chr(self[index])

    def __add__(self, other: bytes) -> "BinaPy":
        """
        Override base method so that addition returns a BinaPy instead of bytes.
        Args:
            other: bytes or BinaPy to add

        Returns:
            a BinaPy
        """
        return self.__class__(super().__add__(other))

    def __radd__(self, other: bytes) -> "BinaPy":
        """
        Override base method so that right addition returns a BinaPy instead of bytes.
        Args:
            other: bytes or BinaPy to radd

        Returns:
            a BinaPy
        """
        return self.__class__(other.__add__(self))

    def split(self, sep: Optional[bytes] = None, maxsplit: int = -1) -> "List[BinaPy]":  # type: ignore[override]
        """
        Override base method so that split() returns a BinaPy instead of bytes.
        Args:
            sep: a separator
            maxsplit: the maximum number of splits

        Returns:
            a BinaPy
        """
        return [self.__class__(b) for b in super().split(sep, maxsplit)]

    def cut_at(self, *pos: int) -> "List[BinaPy]":
        """
        Cut this BinaPy at one or more integer positions.
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
    Extension registry.
    """

    @classmethod
    def get_extension_methods(cls, name: str) -> Dict[str, Callable[..., Any]]:
        extension = cls.extensions.get(name)
        if extension is None:
            raise ValueError(f"Extension {name} not found")
        return extension

    @classmethod
    def get_checker(cls, extension_name: str) -> Callable[..., bool]:
        extension_methods = cls.get_extension_methods(extension_name)
        method = extension_methods.get("check")
        if method is None:
            raise ValueError(
                f"Extension {extension_name} doesn't have a checker method"
            )
        return method

    @classmethod
    def get_decoder(cls, extension_name: str) -> "Callable[..., BinaPy]":
        extension_methods = cls.get_extension_methods(extension_name)
        method = extension_methods.get("decode")
        if method is None:
            raise ValueError(f"Extension {extension_name} doesn't have a decode method")
        return method

    @classmethod
    def get_encoder(cls, extension_name: str) -> "Callable[..., BinaPy]":
        extension_methods = cls.get_extension_methods(extension_name)
        method = extension_methods.get("encode")
        if method is None:
            raise ValueError(
                f"Extension {extension_name} doesn't have an encode method"
            )
        return method

    @classmethod
    def get_parser(cls, extension_name: str) -> Callable[..., Any]:
        extension_methods = cls.get_extension_methods(extension_name)
        method = extension_methods.get("parse")
        if method is None:
            raise ValueError(f"Extension {extension_name} doesn't have a parse method")
        return method

    @classmethod
    def get_serializer(cls, extension_name: str) -> "Callable[..., BinaPy]":
        extension_methods = cls.get_extension_methods(extension_name)
        method = extension_methods.get("serialize")
        if method is None:
            raise ValueError(
                f"Extension {extension_name} doesn't have a serialize method"
            )
        return method

    def encode_to(self, name: str, *args: Any, **kwargs: Any) -> "BinaPy":
        """
        Encodes data from this BinaPy according to the extension format `name`.
        Args:
            name: extension name to use
            *args: additional position parameters for the extension encoder method
            **kwargs: additional keyword parameters for the extension encoder method

        Returns:
            data as returned by the extension encoder method
        """
        encoder = self.get_encoder(name)

        return encoder(self, *args, **kwargs)

    def decode_from(self, name: str, *args: Any, **kwargs: Any) -> "BinaPy":
        """
        Decodes data from this BinaPy according to the format `name`.
        Args:
            name: extension name to use
            *args: additional position parameters for the extension decoder method
            **kwargs: additional keyword parameters for the extension decoder method

        Returns:
            data as returned by the extension
        """
        decoder = self.get_decoder(name)

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
            checker = self.get_checker(name)
            try:
                return checker(self)
            except Exception as exc:
                if raise_on_error:
                    raise exc from exc
                return False
        except ValueError:
            try:
                decoder = self.get_decoder(name)
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

    def check_all(self, decode: bool = False) -> List[str]:
        """
        Checks if this BinaPy conforms to any of the registered extensions.
        Returns: a list of extensions that this BinaPy can be decoded from.

        Args:
            decode: if True, for extensions that don't have a checker method, try to decode this BinaPy using the decoder method to check if that works.
        """

        def get_results() -> Iterator[str]:
            for name in self.extensions:
                success = self.check(name, decode=decode)
                if success is True:
                    yield name

        return list(get_results())

    def parse_from(self, name: str, *args: Any, **kwargs: Any) -> Any:
        """
        Parse data from this BinaPy, based on a given extension format.
        Args:
            name: name of the extension to use
            *args: additional position parameters for the extension decoder method
            **kwargs: additional keyword parameters for the extension decoder method

        Returns:
            the result from parsing this BinaPy
        """
        parser = self.get_parser(name)

        return parser(self, *args, **kwargs)

    @classmethod
    def serialize_to(cls, name: str, *args: Any, **kwargs: Any) -> "BinaPy":
        """
        Serialize (dump) data to a BinaPy, based on a given extension format.
        Args:
            name: name of the extension to use
            *args: additional position parameters for the extension decoder method (which includes the data to serialize)
            **kwargs: additional keyword parameters for the extension decoder method

        Returns:
            a BinaPy, resulting from serialization of the data
        """
        serializer = cls.get_serializer(name)

        return serializer(*args, **kwargs)

    @classmethod
    def register_extension(
        cls, name: str, feature: str, func: Callable[..., Any]
    ) -> None:
        setattr(BinaPy, func.__name__, func)
        ext_dict = cls.extensions.setdefault(name, {})
        ext_dict[feature] = func


F = TypeVar("F", bound=Callable[..., Any])


def binapy_encoder(name: str) -> Callable[[F], F]:
    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> BinaPy:
            raw_result = func(*args, **kwargs)
            if not isinstance(raw_result, (bytes, bytearray, str)):
                raise ValueError(
                    f"extension {name} encoder method did not return binary data"
                )
            return BinaPy(raw_result)

        BinaPy.register_extension(name, "encode", wrapper)
        return cast(F, wrapper)

    return decorator


def binapy_decoder(name: str) -> Callable[[F], F]:
    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> BinaPy:
            raw_result = func(*args, **kwargs)
            if not isinstance(raw_result, (bytes, bytearray)):
                raise ValueError(
                    f"extension {name} decoder method did not return binary data"
                )
            return BinaPy(raw_result)

        BinaPy.register_extension(name, "decode", wrapper)
        return cast(F, wrapper)

    return decorator


def binapy_checker(name: str) -> Callable[[F], F]:
    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> bool:
            raw_result = func(*args, **kwargs)

            if not isinstance(raw_result, bool):
                raise ValueError(
                    f"extension {name} checker method did not return boolean data"
                )
            return raw_result

        BinaPy.register_extension(name, "check", wrapper)
        return cast(F, wrapper)

    return decorator


def binapy_serializer(name: str) -> Callable[[F], F]:
    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> BinaPy:
            raw_result = func(*args, **kwargs)
            if not isinstance(raw_result, (bytes, bytearray)):
                raise ValueError(
                    f"extension {name} serializer method did not return binary data"
                )
            return BinaPy(raw_result)

        BinaPy.register_extension(name, "serialize", wrapper)
        return cast(F, wrapper)

    return decorator


def binapy_parser(name: str) -> Callable[[F], F]:
    def decorator(func: Callable[..., Any]) -> Any:
        BinaPy.register_extension(name, "parse", func)
        return func

    return decorator
