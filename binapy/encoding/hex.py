from binapy import binapy_checker, binapy_decoder, binapy_encoder


@binapy_decoder("hex")
def decode_hex(bp):
    return bytes.fromhex(bp.decode())


@binapy_encoder("hex")
def encode_hex(bp):
    return bp.hex()


@binapy_checker("hex")
def is_hex(bp):
    return (
        len(bp) % 2 == 0
        and bp.isalnum()
        and set(bp.lower()).issubset(b"abcdef0123456789")
    )
