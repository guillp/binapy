import struct

from binapy import binapy_extension


@binapy_extension("struct", decode=True)
def struct_unpack(self, format):
    return struct.unpack(format, self)
