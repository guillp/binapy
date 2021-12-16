# Usage

## import
To use BinaPy in a project, import the main class like this:

```python
from binapy import BinaPy
```

`BinaPy` is a subclass of Python's built-in `bytes`, so you can use it anywhere a `bytes` is required.
You may also `.decode()` it to convert it to a `str`, or use any of the default methods from [`bytes`](https://docs.python.org/3/library/stdtypes.html#bytes)
It also provides a few additional convenience methods such as `cut_at(*pos)`

## initialize
To initialize a `BinaPy`:

- from a `bytes`: `bp = BinaPy(b'my raw bytes \x01\xcf'`)
- from a `str`: `bp = BinaPy("my string", encoding='cp1252')`. If `encoding` is omitted, it will default to `'utf-8'`. That is a different to the `bytes` constructor where encoding is mandatory when you give it a `str` as value.
- from a `bytearray`: `bp = BinaPy(bytearray(b'my bytearray data'))`
- from an `int` array: bp = `BinaPy([109, 121, 32, 105, 110, 116, 32, 97, 114, 114, 97, 121])`
- from an `int`: `bp = BinaPy.from_int(82412341)`. You may additionally pass `size`, `order`, and `signed` parameters, with the same semantics as [`int.to_bytes((length, byteorder, signed=False)`](https://docs.python.org/3/library/stdtypes.html#int.to_bytes). You can do the opposite and convert an BinaPy to an int with `bp.to_int()`.
- with random data, of arbitrary size: `bp = BinaPy.random(32)`. The parameter is the size of the generated data, in bytes.
- from a string containing the binary representation of your data: `bp = BinaPy.from_binary_string('101010')`. The reverse transformation is available with `bp.to_binary_string()`.

## transform
Extensions provide a fluent interface to apply transformations on a BinaPy. For example, to generate a random binary data, hash it with SHA256 then base64url encode the result:
```python
bp = BinaPy.random(128).hash_sha256().encode_b64u()
print(bp)
# b'QTs64tuMZ-TnyYPhjopIryaFPeF26SKKN4y-su2sBYg'
```

Methods that handle encoding or decoding of data return another BinaPy, which makes it possible to chain calls with multiple transformations.

## check
You can check if a BinaPy data conforms with a given extension using the `.check(name)` method.

```python
bp = BinaPy(b"ThisIsData==")
bp.check("b64")
# True
bp.check("hex")
# False
```

You can also check a BinaPy against all extensions using `.check_all()`. For example,
any random 20 bytes could be the result from a SHA1 hash:
```python
bp = BinaPy.random(20)
bp.check_all()
# ['sha1']
```

While a given string with only hex characters could be a hexadecimal string, it could also be the result of a base64
or a base64url encoding.
```python
bp = BinaPy("abcdef1234567890")
bp.check_all()
# ['b64', 'b64u', 'hex']
# ['b64', 'b64u', 'hex']
```
## load and dump
Dumping and encoding data can be done this way:
```python
BinaPy.from_json({"foo": "bar"}).encode_b64u()
# b'ewoiZm9vIjogImJhciIKfQ'
```
Loading serialized and encoded data can be done this way:
```python
BinaPy(b"ewoiZm9vIjogImJhciIKfQ").decode_b64u().parse_json()
# {'foo': 'bar'}
```

## extend
You can implement additional methods for BinaPy. Methods can implement one or several of the following features:

- an *encoder*: this will transform/encode the current BinaPy into another BinaPy. E.g., a base64 encoder will transform arbitrary binary data into a base64 encoded string.
- a *decoder*: this will transform an encoded data back into its initial data. E.g., a base64 decoder.
- a *checker*: this will check if a given data conforms to a given format. Which means that this data could have been produced with a matching *encoder* and can probably be decoded with the matching *decoder*, if available.
- a *parser*: this will parse the current BinaPy data into another format. E.g., a JSON parser
- a *serializer*: this will serialize data from another format into a BinaPy. E.g, a JSON dumper

Note that the terms *encode* and *decode* are quite loose, because they are applied to compression, hashing and other transformations that produce or consume binary data.

To implement such a method, use one of the `binapy_<feature>()` decorator. It takes the name of the extension as parameter.

```python
from binapy import binapy_encoder


@binapy_encoder("myformat")
def encode_myformat(bp) -> bytes:
    # apply your transformation
    return my_transformation(bp)
```

This `binapy_encoder()` decorator will:

- register this method in BinaPy extension registry, so that it can be called with `BinaPy(my_data).encode_to('myformat')`.
- add this method to BinaPy with a `setattr()`, so that it can be called with `BinaPy(my_data).encode_myformat()` (same name as the decorated method).
- if that methods returns a `bytes` or a `bytesarray`, make sure that it returns a `BinaPy` instead, to make sure it is fluent.

Some formats such as *base64* can have all 3 methods implemented. Others such as hashes only have an encoder and checker method:

- the encoder does the actual hashing (that is, by definition, irreversible)
- the checker method checks that a given data is the appropriate length for the given hash

Finally, some formats like *gzip* do not have a checker method, because trying to decode the data is faster and easier than validating it statically.
BinaPy will then try the decode method instead and see if it raises an Exception.
