import json

def print_indented(x):
    print(json.dumps(x, sort_keys=True, indent=4))
