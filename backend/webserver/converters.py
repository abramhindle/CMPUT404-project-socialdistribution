import webserver.models as models

class Converter(object):
    def __init__(self) -> None:
        self.expected_status_codes = {
            "check_for_follower": 200,
            "send_follow_request": 201,
            "send_post_inbox": 201,
        }

    # returns the request payload required for sending a follow request
    def send_follow_request(self, request_data):
        return request_data
    
    # returns the request payload required for sending a post inbox
    def send_post_inbox(self, remote_author, post_id):
        payload = {
            "type": "post",
            "post": {
                "id": f"{post_id}",
            }
        }
        if isinstance(remote_author, models.RemoteAuthor):
            payload["post"]["author"] = {
                "id": f"{remote_author.id}",
                "url": f"{remote_author.get_absolute_url()}",
            }
        elif isinstance(remote_author, dict):
            payload["post"]["author"] = {
                "id": remote_author["id"],
                "url": remote_author["url"]
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


class Team11Converter(Converter):
    def send_follow_request(self, request_data):
        raise NotImplementedError   # TODO
    
    def send_post_inbox(self, remote_author, post_id):
        raise NotImplementedError   # TODO
    
    def convert_author(self, data: dict):
        raise NotImplementedError   # TODO
    
    def convert_post(self, data: dict):
        raise NotImplementedError  # TODO
