# BinaPy

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Downloads](https://pepy.tech/badge/binapy/month)](https://pepy.tech/project/binapy)
[![Supported Versions](https://img.shields.io/pypi/pyversions/binapy.svg)](https://pypi.org/project/binapy)
[![PyPi license](https://badgen.net/pypi/license/binapy/)](https://pypi.com/project/binapy/)
[![PyPI status](https://img.shields.io/pypi/status/binapy.svg)](https://pypi.python.org/pypi/binapy/)
[![GitHub commits](https://badgen.net/github/commits/guillp/binapy)](https://github.com/guillp/binapy/commit/)
[![GitHub latest commit](https://badgen.net/github/last-commit/guillp/binapy)](https://github.com/guillp/binapy/commit/)

**BinaPy** is a module that makes Binary Data manipulation simpler and easier than what is offered in the Python standard library.

With BinaPy, encoding or decoding data in a number of formats (base64, base64url, hex, url-encoding, etc.), compressing or decompressing (gzip), hashing (SHA1, SHA256, MD5, etc., with or without salt), is all a single method call away! And you can extend it with new formats and features.

```python
from binapy import BinaPy

bp = BinaPy("Hello, World!").to("gzip").to("b64u")
print(bp)
# b'eJzzSM3JyddRCM8vyklRBAAfngRq'
bp.decode_from("b64u").decode_from("gzip").decode()
# "Hello, World!"
isinstance(bp, bytes)
# True
```

* Free software: MIT
* Documentation: <https://guillp.github.io/binapy/>

## Features

- Fluent interface, based on a `bytes` subclass
- Provides a convenient interface over `hashlib`, `base64`, `gzip`, `urllib.parse`, `json` and more
- Easy to extend with new formats

## TODO

- add more parsing formats like YAML, CBOR, etc.
- optionally use faster third-party modules when available

## Credits

This package template was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [zillionare/cookiecutter-pypackage](https://github.com/zillionare/cookiecutter-pypackage) project template.
