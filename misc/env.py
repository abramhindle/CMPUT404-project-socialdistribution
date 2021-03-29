import json
import base64
import gen

x = '''
{
    "team4": {
        "domain": "",
        "port": "443",
        "scheme": "https://",
        "username": "team4",
        "password": "team44maet"
    },
    "team20": {
        "domain": "",
        "port": "443",
        "scheme": "https://",
        "username": "team20",
        "password": "team2002maet"
    },
    "clone": {
        "domain": "",
        "port": "443",
        "scheme": "https://",
        "username": "clone",
        "password": "cloneenolc"
    },
    "self": {
        "domain": "socdist-t1.herokuapp.com",
        "port":"443",
        "scheme": "https://"
    }
}
'''

x = json.loads(x)
compact_x = {}

for key in x.keys():
    if key == "self":
        compact_x[key] = {"domain": x[key]["scheme"] + x[key]["domain"], "port": x[key]["port"]}    
    else:
        compact_x[key] = {"url": x[key]["scheme"] + x[key]["domain"], "port": x[key]["port"], "auth": gen.generateBasicAuth(x[key]["username"], x[key]["password"])}
print(base64.b64encode(json.dumps(compact_x).encode('utf-8')).decode('utf-8'))