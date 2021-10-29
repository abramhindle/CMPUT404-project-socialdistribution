from urllib.parse import urlsplit
from cmput404.constants import HOST, API_PREFIX


class UrlParser():

    def is_local_url(self, url):
        """ Check that a URL is hosted on the local server. If not, return a ValueError.
        """

        o = urlsplit(url)
        host = o.netloc
        return host == HOST

    def parse_author(self, url):
        """ Parse the URL of a local author and return the author_id. Throws value error if the URL
            is not hosted on the local server.
        """

        o = urlsplit(url)
        path_components = o.path.strip('/').split('/')
        if path_components[0] == API_PREFIX:
            path_components.pop(0)

        if len(path_components) != 2 or path_components[0] != "author":
            raise ValueError("URL does not match format of author ID")

        return path_components[1]

    def parse_post(self, url):
        """ Parse the URL of a local post and return the author_id, post_id. Throws value error if the URL
            is not hosted on the local server.
        """

        o = urlsplit(url)
        path_components = o.path.strip('/').split('/')
        if path_components[0] == API_PREFIX:
            path_components.pop(0)

        if len(path_components) != 4 or path_components[0] != "author" or path_components[2] != "posts":
            raise ValueError("URL does not match format of post ID")

        return path_components[1], path_components[3]


url_parser = UrlParser()
