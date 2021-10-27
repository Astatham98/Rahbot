import json


def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)