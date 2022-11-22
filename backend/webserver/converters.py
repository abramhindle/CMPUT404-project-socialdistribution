import webserver.models as models
from .utils import join_urls, get_host_from_absolute_url
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
    
    def url_to_send_post_inbox_at(self, author_url):
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

    def public_posts_url(self, api_url):
        return join_urls(api_url, "posts", ends_with_slash=True)
    
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
    
    def public_posts_url(self, api_url):
        return None
    
    def convert_author(self, data: dict):
        raise NotImplementedError   # TODO
    
    def convert_post(self, data: dict):
        raise NotImplementedError  # TODO

class Team10Converter(Converter):
    def __init__(self):
        super().__init__()
        self.expected_status_codes["send_follow_request"] = 200
        self.expected_status_codes["send_post_inbox"] = 200
        
    def skip_follow_check_before_sending_follow_request(self):
        return True

    def url_to_send_follow_request_at(self, author_url):
        return join_urls(author_url, "followers", ends_with_slash=True)
    
    def url_to_send_post_inbox_at(self, author_url):
        return join_urls(author_url, "inbox")
    
    def public_posts_url(self, api_url):
        return join_urls(api_url, "posts/public", ends_with_slash=True)
    
    def send_follow_request(self, request_data):
        converted_data = {
            "actor": request_data["sender"]["url"]
        }
        return converted_data
    
    def send_post_inbox(self, post, request: HttpRequest):
        host = get_host_from_absolute_url(post.author.get_url(request))
        converted_data = {
            "author":{
                "type": "author",
                "id": f"{post.author.id}",
                "url": post.author.get_url(request),
                "host": host,
                "displayName": f"{post.author.display_name}",
                "github": f"{post.author.github_handle}",
                "profileImage": f"{post.author.profile_image}"
            },
            "type": "post",
            "id": f"{post.id}",
            "url": post.get_url(request),
            "title": post.title,
            "description": post.description,
            "visibility": post.visibility.lower(),
            "source": post.source,
            "origin": post.origin,
            "contentType": post.content_type,
            "unlisted": post.unlisted,
            "count": 0,                         # TODO: update once we support comments
            "comments":"www.default.com",       # TODO: update once we support comments
            "published": f"{post.created_at}"
        }
        return converted_data
        
    def convert_author(self, data: dict):
        converted_data ={
            "url": data["url"],
            "id": data["id"],
            "display_name": data["displayName"],
            "profile_image": data["profileImage"],
            "github_handle": data["github"],
        }
        return converted_data

    def convert_authors(self, data):
        if "items" in data:
            return [self.convert_author(author) for author in data["items"]]
        return None
    
    def convert_post(self, data: dict):
        converted_data = {
            "id": data["id"],
            "author":{
                "url": data["author"]["url"],
                "id": data["author"]["id"],
                "display_name": data["author"]["displayName"],
                "profile_image": data["author"]["profileImage"],
                "github_handle": data["author"]["github"]
            },
            "created_at": data["published"],
            "edited_at": None,
            "title": data["title"],
            "description": data["description"],
            "visibility": data["visibility"].upper(),
            "source": data["source"],
            "origin":data["origin"],
            "unlisted":data["unlisted"],
            "content_type": data["contentType"],
            "content": None,
            "likes_count": 0
        }
        return converted_data

    def convert_posts(self,data):
        if "items" in data:
            return [self.convert_post(post) for post in data["items"]]
        return None
