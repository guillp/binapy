from urllib.parse import quote, unquote, unquote_plus

from binapy import binapy_extension


@binapy_extension("url", encode=True)
def url_encode(self, safe="/"):
    return quote(self, safe=safe)


@binapy_extension("url", decode=True)
def url_decode(self, spaces=True, errors="replace"):
    if spaces:
        return unquote_plus(self, errors=errors)
    else:
        return unquote(self, errors=errors)
