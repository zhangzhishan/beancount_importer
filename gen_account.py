import json
import sys
import os
import io
import sys
from os import path

def load_json(filename):
    fd = open(filename, 'r', encoding="UTF-8")
    data = fd.read()
    js = json.loads(data)
    fd.close()
    return js

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    mappings = load_json(path.join(os.path.dirname(os.path.realpath(__file__)), 'map.json'))
    for key, mapping in mappings.items():
        if key == "expenses":
            for account in mapping.values():
                print("1970-01-01 open Expenses:" + account)
        else:
            if key != "tags":
                for account in mapping.values():
                    print("1970-01-01 open " + account)

