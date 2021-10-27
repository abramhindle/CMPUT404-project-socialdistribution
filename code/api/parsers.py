from urllib.parse import urlsplit
from cmput404.constants import HOST, API_PREFIX


class LocalUrlParser():

    def assert_local_url(self, url):
        """ Check that a URL is hosted on the local server. If not, return a ValueError.
        """

        o = urlsplit(url)
        host = o.netloc
        if (host != HOST):
            raise ValueError("URL ID does not match local host")

    def parse_author(self, url):
        """ Parse the URL of a local author and return the author_id. Throws value error if the URL
            is not hosted on the local server.
        """

        self.assert_local_url(url)

        o = urlsplit(url)
        path_components = o.path.strip('/').split('/')
        if path_components[0] == API_PREFIX[:-2]:
            path_components.pop(0)

        if len(path_components) != 2 or path_components[0] != "author":
            raise ValueError("URL does not match format of author ID")

        return path_components[1]


local_url_parser = LocalUrlParser()
