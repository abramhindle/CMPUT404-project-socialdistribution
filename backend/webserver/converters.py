import webserver.models as models
from .utils import join_urls
import logging
from django.http.request import HttpRequest

logger = logging.getLogger(__name__)

class Converter(object):
    def __init__(self) -> None:
        self.expected_status_codes = {
            "check_for_follower": 200,
            "send_follow_request": 201,
            "send_post_inbox": 201,
        }
    
    def url_to_send_follow_request_at(self, author_url):
        return join_urls(author_url, "inbox", ends_with_slash=True)

    # returns the request payload required for sending a follow request
    def send_follow_request(self, request_data):
        return request_data
    
    def skip_follow_check_before_sending_follow_request(self):
        return False
    
    # returns the request payload required for sending a post inbox
    # the passed post is a local post
    def send_post_inbox(self, post, request: HttpRequest):
        payload = {
            "type": "post",
            "post": {
                "id": f"{post.id}",
                "author": {
                    "id": f"{post.author.id}",
                    "url": post.author.get_url(request),
                }
            }
        }
        return payload
    
    def remote_follow_request_sender_id(self, serialized_data):
        id = serialized_data["sender"]["id"]
        if "authors" in id:
            # e.g. "http://127.0.0.1:5454/authors/1d698d25ff008f7538453c120f581471"
            id_section = id.split("authors")[1]
            return id_section.split("/")[0].strip("/")
        return id

    def expected_status_code(self, use_case_name):
        return self.expected_status_codes.get(use_case_name, 200)
    
    # converts a remote author's response to the format specified by AuthorSerializer
    def convert_author(self, data: dict):
        return data
    
    def convert_authors(self, data):
        if isinstance(data, list):
            return [self.convert_author(author) for author in data]
        else:
            # data must be in paginated form
            if "results" in data:
                return [self.convert_author(author) for author in data["results"]]
        return None
    
    # converts a remote post's response to the format specified by PostSerializer
    def convert_post(self, data: dict):
        return data
    
    def convert_posts(self, data):
        if isinstance(data, list):
            return [self.convert_post(post) for post in data]
        else:
            # data must be in paginated form
            if "results" in data:
                for i in range(len(data["results"])):
                    data["results"][i] = self.convert_post(data["results"][i])
                return data
        return None


class Team11Converter(Converter):
    def send_follow_request(self, request_data):
        raise NotImplementedError   # TODO
    
    def send_post_inbox(self, post, request: HttpRequest):
        raise NotImplementedError   # TODO
    
    def convert_author(self, data: dict):
        raise NotImplementedError   # TODO
    
    def convert_post(self, data: dict):
        raise NotImplementedError  # TODO


class Team10Converter(Converter):
    def skip_follow_check_before_sending_follow_request(self):
        return True

    def url_to_send_follow_request_at(self, author_url):
        return join_urls(author_url, "followers", ends_with_slash=True)
