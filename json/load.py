import json

for encodedjson in open('json.txt'):
    decodejson = json.loads(encodedjson)
    print type(decodejson)
    print decodejson
