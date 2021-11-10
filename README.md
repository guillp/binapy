# BinaPy


<p align="center">
<a href="https://pypi.python.org/pypi/binapy">
    <img src="https://img.shields.io/pypi/v/binapy.svg"
        alt = "Release Status">
</a>

<a href="https://github.com/guillp/binapy/actions">
    <img src="https://github.com/guillp/binapy/actions/workflows/main.yml/badge.svg?branch=release" alt="CI Status">
</a>

<a href="https://binapy.readthedocs.io/en/latest/?badge=latest">
    <img src="https://readthedocs.org/projects/binapy/badge/?version=latest" alt="Documentation Status">
</a>

<a href="https://pyup.io/repos/github/guillp/binapy/">
<img src="https://pyup.io/repos/github/guillp/binapy/shield.svg" alt="Updates">
</a>

</p>


**BinaPy** is a module that makes Binary Data manipulation simpler and easier than what is offered in the Python standard library.

With BinaPy, encoding or decoding data in a number of formats (base64, base64url, hex, url-encoding, etc.), compressing or decompressing (gzip), hashing (SHA1, SHA256, MD5, etc., with or without salt), is all a single method call away! And you can extend it with new formats and features.

```python
from binapy import BinaPy

bp = BinaPy("Hello, World!").compress_gzip().encode_b64u()
print(bp)
# b'eJzzSM3JyddRCM8vyklRBAAfngRq'
bp.decode_b64u().decompress_gzip().decode()
# "Hello, World!"
isinstance(bp, bytes)
# True
```

* Free software: MIT
* Documentation: <https://binapy.readthedocs.io>

## Features

- Fluent interface, based on a `bytes` subclass
- Provides a convenient interface over `hashlib`, `base64`, `gzip`, `urllib.parse`, `json` and more
- Easy to extend with new formats

## TODO

- add more parsing formats like YAML, CBOR, etc.
- optionally use faster third-party modules when available

## Credits

This package template was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [zillionare/cookiecutter-pypackage](https://github.com/zillionare/cookiecutter-pypackage) project template.
