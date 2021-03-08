from urllib.parse import urlparse

def getSafeURL(absolute_uri):
  parsed_url = urlparse(absolute_uri)
  host = ""
  if parsed_url.port:
      # if port exist, keep it as-is
      host = '{url.scheme}://{url.hostname}:{url.port}'.format(url=parsed_url)
  else:
      # port does not exist, decide default port by scheme
      if parsed_url.scheme == 'http':
          host = 'http://{url.hostname}:80'.format(url=parsed_url)
      elif parsed_url.scheme == 'https':
          host = 'https://{url.hostname}:443'.format(url=parsed_url)
      else:
          # neither port exist nor scheme recognized, treat it as https with port 443
          # since we only support http/https
          host = 'https://{url.hostname}:443'.format(url=parsed_url)
  return host