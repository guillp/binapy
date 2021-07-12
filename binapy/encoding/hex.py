from binapy import binapy_extension


@binapy_extension("hex", decode=True)
def decode_hex(self):
    return bytes.fromhex(self.decode())


@binapy_extension("hex", encode=True)
def encode_hex(self):
    return self.hex()
