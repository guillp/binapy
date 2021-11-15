from urllib.parse import quote, quote_plus, unquote, unquote_plus

from binapy import binapy_decoder, binapy_encoder


@binapy_encoder("url")
def url_encode(bp: str, safe: str = "/", plus_spaces: bool = True) -> str:
    if plus_spaces:
        return quote_plus(bp, safe=safe)
    else:
        return quote(bp, safe=safe)


@binapy_decoder("url")
def url_decode(bp: bytes, plus_spaces: bool = True, errors: str = "replace") -> bytes:
    if plus_spaces:
        return unquote_plus(bp.decode(), errors=errors).encode()
    else:
        return unquote(bp.decode(), errors=errors).encode()
