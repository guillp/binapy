import json

from binapy import binapy_extension


@binapy_extension("json", decode=True)
def parse_json(self):
    return json.loads(self)


@binapy_extension("json", encode=True)
def from_json(self, data, indent=0):
    return json.dumps(data, indent=indent)
