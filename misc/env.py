import json
import base64
import gen

x = '''
{
    "team4": {
        "domain": "c404posties.herokuapp.com",
        "port": "443",
        "scheme": "https://",
        "auth": "Token 49998f0a42dbd0ec33787c88823d5bd32dd3778a"
    },
    "team20": {
        "domain": "",
        "port": "443",
        "scheme": "https://",
        "auth": ""
    },
    "clone": {
        "domain": "social-distribution-t1v2.herokuapp.com",
        "port": "443",
        "scheme": "https://",
        "auth": "Basic UmVtb3RlMTpyZW1vdGUxMjM0"
    },
    "self": {
        "domain": "social-distribution-t1.herokuapp.com",
        "port":"443",
        "scheme": "https://"
    }
}
'''

x = json.loads(x)
compact_x = {}

for key in x.keys():
    if key == "self":
        compact_x[key] = {"domain": x[key]["scheme"] +
                          x[key]["domain"], "port": x[key]["port"]}
    else:
        compact_x[key] = {"url": x[key]["scheme"] + x[key]
                          ["domain"], "port": x[key]["port"], "auth": x[key]["auth"]}
print(base64.b64encode(json.dumps(compact_x).encode('utf-8')).decode('utf-8'))
