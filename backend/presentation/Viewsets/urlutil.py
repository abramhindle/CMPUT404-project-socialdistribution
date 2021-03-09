from urllib.parse import urlparse

def getSafeURL(absolute_uri):
  parsed_url = urlparse(absolute_uri)
  host = ""
  if parsed_url.port:
      # if port exist, keep it as-is
      host = '{url.scheme}://{url.hostname}:{url.port}'.format(url=parsed_url)
  else:
      # port does not exist
      if parsed_url.scheme == 'http':
          host = 'http://{url.hostname}'.format(url=parsed_url)
      else:
          host = 'https://{url.hostname}'.format(url=parsed_url)
  return host