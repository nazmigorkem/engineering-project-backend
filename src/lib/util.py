import json

class Util:

    def dump(path: str, item):
        json_dump = json.dumps(item, indent=2)
        with open(path, "w") as out_f:
            out_f.write(json_dump)
