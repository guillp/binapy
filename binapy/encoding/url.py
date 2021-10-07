from urllib.parse import quote, unquote, unquote_plus

from binapy import binapy_decoder, binapy_encoder


@binapy_encoder("url")
def url_encode(self, safe="/"):
    return quote(self, safe=safe)


@binapy_decoder("url")
def url_decode(self, spaces=True, errors="replace"):
    if spaces:
        return unquote_plus(self, errors=errors)
    else:
        return unquote(self, errors=errors)
