import json

class Jprint():
    def jprint(self, obj):
        text = json.dumps(obj, sort_keys=True, indent=4)
        print(text)