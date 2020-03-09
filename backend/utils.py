from urllib.parse import urlparse

def protocol_removed(url):
    parsed_url = urlparse(url)
    scheme = "%s://" % parsed_url.scheme
    url = parsed_url.geturl().replace(scheme, '', 1)

    return url