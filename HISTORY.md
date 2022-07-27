# History

## 0.3.0 (2021-11-15)

- Renaming `serialize_from()` to `serialize_to()` and `parse_to()` to `parse_from()`.

## 0.2.0 (2021-11-10)

- Serialize JSON as compact by default
- `datetime` instances are serialized to epoch timestamps when serializing JSON (but they are not converted back on parsing).
- add `.to_int()` to convert a BinaPy to an int.

## 0.1.0 (2021-07-08)

- First release on PyPI.
