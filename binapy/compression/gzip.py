import zlib

from binapy import binapy_extension


@binapy_extension("gzip", encode=True)
def compress_gzip(self, level=-1):
    return zlib.compress(self)


@binapy_extension("gzip", decode=True)
def decompress_gzip(self):
    return zlib.decompress(self)
