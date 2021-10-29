import requests

# make an http requests and handle status codes
def make_request(method='GET', url='http://127.0.0.1:8000/', body=''):
    """
    Makes an HTTP request
    """
    r = None
    print(method, url, body)
    if method == 'GET':
        r = requests.get(url)
    elif method == 'POST':
        r = requests.post(url, data=body)
    #todo: handle status codes