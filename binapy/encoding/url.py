from urllib.parse import quote, quote_plus, unquote, unquote_plus

from binapy import binapy_decoder, binapy_encoder


@binapy_encoder("url")
def url_encode(bp, safe="/", plus_spaces=True):
    if plus_spaces:
        return quote_plus(bp, safe=safe)
    else:
        return quote(bp, safe=safe)


@binapy_decoder("url")
def url_decode(bp, plus_spaces=True, errors="replace"):
    if plus_spaces:
        return unquote_plus(bp.decode(), errors=errors).encode()
    else:
        return unquote(bp.decode(), errors=errors).encode()
