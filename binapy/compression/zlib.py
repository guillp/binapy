import zlib

from binapy import binapy_decoder, binapy_encoder


@binapy_encoder("zlib")
def compress_zlib(bp: bytes, level: int = 6) -> bytes:
    return zlib.compress(bp, level)


@binapy_decoder("zlib")
def decompress_zlib(bp: bytes) -> bytes:
    return zlib.decompress(bp)


@binapy_encoder("deflate")
def compress_saml(bp: bytes, level: int = -1) -> bytes:
    return zlib.compress(bp, level=level)[
        2:-4
    ]  # removes the 2 bytes zlib header and the final 4 bytes Adler checksum


@binapy_decoder("deflate")
def decompress_saml(bp: bytes, bufsize: int = zlib.DEF_BUF_SIZE) -> bytes:
    return zlib.decompress(bp, wbits=-15, bufsize=bufsize)
