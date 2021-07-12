# Usage

To use BinaPy in a project, import the main class like this:

```
    from binapy import BinaPy
```

`BinaPy` is a subclass of Python's built-in `bytes`, so you can use it anywhere a `bytes` is required.

To initalize a `BinaPy`:
- with a `bytes`: `bp = BinaPy(b'my raw bytes \x01\xcf`
- with a `str`: `bp = BinaPy("my string", encoding='cp1252')`. If `encoding` is omitted, it will default to `'utf-8'`.
- with an `int`: `bp = BinaPy.from_int(82412341)`. You may additionally pass `size`, `order`, and `signed` parameters, with the same semantics as [`int.to_bytes((length, byteorder, signed=False)`](https://docs.python.org/3/library/stdtypes.html#int.to_bytes)
