from binapy import BinaPy


def test_deflate() -> None:
    assert BinaPy(
        "fVNNj9owFLxX6n+wfCdxskAaC6go9AOJQkRoD71Urv1SLMV2aju79N/XycIqldqcLNkz82bee144puqGrlt/0Sf41YLz6Kpq7Wj/sMSt1dQwJx3VTIGjntNy/XlP04jQxhpvuKnxgDLOYM6B9dJojHbbJT4e3u+PH3eH729InpGsIuSBsJkgZJ4SnotcVHlWzdOMVZALztMpRl/BusBf4iCHUWHNoxRgD6HSEpcF8iFA0HauhZ12nmkfkCSZTkg2Sebn9IHOUjqdfcNoG5BSM9+LXbxvaBxL0URwZaqpIeJGxWV5LME+Sg5Rc2n6cn3gd1ILqX+OZ/3xDHL00/lcTIpjecZofc+/Mdq1CuxN/stp/2LC/e1BgDJJHLTg2pl4y7jDq9evEFp07aZ9VLsa4yrwTDDPOvoiHrJeZBradXC3LUwt+W/0wVjF/P/jJVHS30gxqXooBcVkvRbCgnMhZl2bp40F5sNUvG0Bx8Nat0UD0a9daIWHq0cboxpmpevmEUJw/xzzHnSI3dRhkU5QrUZ3jVPe4cJ1EY4nY0U3P+Ch8Nky7Rpj/a0f/xTvHccjlgPi/j78QKs/"
    ).decode_from("b64").decode_from("deflate") == (
        b'<samlp:AuthnRequest xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol" xmlns'
        b':saml="urn:oasis:names:tc:SAML:2.0:assertion" ID="ONELOGIN_809707f0030a5d006'
        b'20c9d9df97f627afe9dcc24" Version="2.0" ProviderName="SP test" IssueInstant="'
        b'2014-07-16T23:52:45Z" Destination="http://idp.example.com/SSOService.php" Pr'
        b'otocolBinding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST" AssertionCons'
        b'umerServiceURL="http://sp.example.com/demo1/index.php?acs">\r\n  <saml:Iss'
        b"uer>http://sp.example.com/demo1/metadata.php</saml:Issuer>\r\n  <samlp:Nam"
        b'eIDPolicy Format="urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress" Al'
        b'lowCreate="true"/>\r\n  <samlp:RequestedAuthnContext Comparison="exact">\r\n'
        b"    <saml:AuthnContextClassRef>urn:oasis:names:tc:SAML:2.0:ac:classes:Passwo"
        b"rdProtectedTransport</saml:AuthnContextClassRef>\r\n  </samlp:RequestedAut"
        b"hnContext>\r\n</samlp:AuthnRequest>"
    )

    assert BinaPy("<this_is_a_test/>").to("deflate").to("hex") == b"b329c9c82c8e07a2c4f892d4e2127d3b00"


def test_zlib() -> None:
    assert BinaPy(b"this is a test").to("zlib", level=9).hex() == "78da2bc9c82c5600a2448592d4e2120026330516"
    assert (
        BinaPy("78da2bc9c82c5600a2448592d4e2120026330516").decode_from("hex").decode_from("zlib") == b"this is a test"
    )
