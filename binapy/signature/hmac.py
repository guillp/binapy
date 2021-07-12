from binapy import binapy_extension


@binapy_extension("hmac", encode=True)
def sign_hmac_sha256(self, secret):
    raise NotImplementedError()
