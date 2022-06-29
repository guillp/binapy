import zlib

from binapy import binapy_decoder, binapy_encoder


@binapy_encoder("gzip")
def compress_gzip(bp: bytes, level: int = -1) -> bytes:
    return zlib.compress(bp, level=level)


@binapy_decoder("gzip")
def decompress_gzip(
    bp: bytes, wbits: int = zlib.MAX_WBITS, bufsize: int = zlib.DEF_BUF_SIZE
) -> bytes:
    return zlib.decompress(bp, wbits=wbits, bufsize=bufsize)


@binapy_encoder("saml")
def compress_saml(bp: bytes, level: int = -1) -> bytes:
    return zlib.compress(bp, level=level)[2:-4]


@binapy_decoder("saml")
def decompress_saml(bp: bytes, bufsize: int = zlib.DEF_BUF_SIZE) -> bytes:
    return zlib.decompress(bp, wbits=-15, bufsize=bufsize)
