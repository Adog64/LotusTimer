import json
from os import path

p = path.split(path.dirname(__file__))[0] + '/assets/data.json'
with open(p) as f:
    data = json.load(f)
    data['id'] = 134 # <--- add `id` value.
    f.seek(0)        # <--- should reset file position to the beginning.
    json.dump(data, f, indent=4)
    f.truncate()     # remove remaining part