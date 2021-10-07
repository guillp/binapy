from binapy import binapy_checker, binapy_decoder, binapy_encoder


@binapy_decoder("hex")
def decode_hex(bp: bytes) -> bytes:
    return bytes.fromhex(bp.decode())


@binapy_encoder("hex")
def encode_hex(bp: bytes) -> bytes:
    return bp.hex().encode()


@binapy_checker("hex")
def is_hex(bp: bytes) -> bool:
    return (
        len(bp) % 2 == 0
        and bp.isalnum()
        and set(bp.lower()).issubset(b"abcdef0123456789")
    )
