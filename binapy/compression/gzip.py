import zlib

from binapy import binapy_decoder, binapy_encoder


@binapy_encoder("gzip")
def compress_gzip(bp: bytes, level: int = -1) -> bytes:
    return zlib.compress(bp, level=level)


@binapy_decoder("gzip")
def decompress_gzip(bp: bytes) -> bytes:
    return zlib.decompress(bp)
