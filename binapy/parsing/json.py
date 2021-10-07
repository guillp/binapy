import json

from binapy import binapy_dumper, binapy_loader


@binapy_loader("json")
def to_json(self):
    return json.loads(self)


@binapy_dumper("json")
def from_json(data, indent=0):
    return json.dumps(data, indent=indent)
